from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import yaml

from .item_scraper import item_scraper
from .item_scraper.validators import ValidationError as ScraptTaskValidationError
from .models import ScrapingTask

deals = [
    {
        'title': 'Szorty kąpielowe',
        'price': '19.99',
        'date_found': '2018-12-01'
    },
    {
        'title': 'Super Blouse',
        'price': '29.99',
        'date_found': '2018-11-04'
    },
    {
        'title': 'Super gacie',
        'price': '9.99',
        'date_found': '2018-12-05'
    },
    {
        'title': 'Super onesie',
        'price': '129.99',
        'date_found': '2018-12-04'
    },
]*2


def home(request):
    if request.user.is_authenticated:
        context = {
            'deals': deals
        }
        return render(request, 'scraper/home.html', context=context)
    else:
        return render(request, 'scraper/home_empty.html')


def test_site(request):
    context = {
        'deals': deals
    }
    return render(request, 'scraper/test_site.html', context=context)


class ScrapingTaskListView(LoginRequiredMixin, ListView):
    model = ScrapingTask
    context_object_name = 'tasks'
    ordering = ['url']
    paginate_by = 10


class ScrapingTaskDetailView(LoginRequiredMixin, DetailView):
    model = ScrapingTask


class ScrapingTaskCreateView(LoginRequiredMixin, CreateView):
    model = ScrapingTask
    fields = [
        'url',
        'active',
        'multiple',
        'task',
        'running_time',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ScrapingTaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ScrapingTask
    fields = [
        'url',
        'active',
        'multiple',
        'running_time',
        'task',
        'description',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        scraping_task = self.get_object()

        if self.request.user == scraping_task.user:
            return True
        else:
            return False


class ScrapingTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ScrapingTask
    success_url = '/scraping-tasks/'

    def test_func(self):
        scraping_task = self.get_object()

        if self.request.user == scraping_task.user:
            return True
        else:
            return False


@login_required
def scraping_task_test_run(request, pk):
    scraping_task = get_object_or_404(ScrapingTask, pk=pk)
    task = yaml.safe_load(scraping_task.task)

    try:
        results, page_source = item_scraper.scrap(
            url=scraping_task.url,
            task=task,
            chromedriver_path=settings.SCRAPER_CHROMEDRIVER_PATH
        )
    except ScraptTaskValidationError as exception:
        messages.warning(request, str(exception))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    result_yamled = [
        yaml.dump(r, default_flow_style=False, allow_unicode=True)
        for r in results
    ]
    context = {
        'scraping_task': scraping_task,
        'results': result_yamled,
    }
    return render(request, 'scraper/scrapingtask_test_run.html', context=context)
