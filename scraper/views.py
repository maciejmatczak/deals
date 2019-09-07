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
from .forms import (ScrapingJobCreateForm, ScrapingJobUpdateForm)
from .models import ScrapingJob, ScrapingTask

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


def test_request_vs_object_user(view):
    object_ = view.get_object()

    if view.request.user == object_.user:
        return True
    else:
        return False


class ScrapingTaskListView(LoginRequiredMixin, ListView):
    model = ScrapingTask
    ordering = ['favourite', 'title']
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return ScrapingTask.objects.filter(user=user)


class ScrapingTaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ScrapingTask

    def test_func(self):
        return test_request_vs_object_user(self)


class ScrapingTaskCreateView(LoginRequiredMixin, CreateView):
    model = ScrapingTask
    fields = [
        'title',
        'favourite',
        'task',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ScrapingTaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ScrapingTask
    fields = [
        'title',
        'favourite',
        'task',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return test_request_vs_object_user(self)


class ScrapingTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ScrapingTask
    success_url = '/scraping-tasks/'

    def test_func(self):
        return test_request_vs_object_user(self)


class ScrapingJobListView(LoginRequiredMixin, ListView):
    model = ScrapingJob
    context_object_name = 'tasks'
    ordering = ['url']
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return ScrapingJob.objects.filter(user=user)


class ScrapingJobDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ScrapingJob

    def test_func(self):
        return test_request_vs_object_user(self)


class ScrapingJobCreateView(LoginRequiredMixin, CreateView):
    model = ScrapingJob
    form_class = ScrapingJobCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ScrapingJobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ScrapingJob
    form_class = ScrapingJobUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return test_request_vs_object_user(self)


class ScrapingJobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ScrapingJob
    success_url = '/scraping-jobs/'

    def test_func(self):
        return test_request_vs_object_user(self)


@login_required
def scraping_job_test_run(request, pk):
    scraping_job = get_object_or_404(ScrapingJob, pk=pk)
    task = yaml.safe_load(scraping_job.scraping_task.task)

    try:
        results, page_source = item_scraper.scrap(
            url=scraping_job.url,
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
        'scraping_job': scraping_job,
        'results': result_yamled,
    }
    return render(request, 'scraper/scrapingjob_test_run.html', context=context)
