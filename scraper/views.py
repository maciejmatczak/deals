from django.db.models import Max
from django.conf import settings
from django.core.paginator import Paginator
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
from typing import NamedTuple
from random import random

from .item_scraper import item_scraper
from .item_scraper.validators import ValidationError as ScrapTaskValidationError
from .forms import ScrapingJobForm
from .models import ScrapingJob, ScrapingTask, Item


def test_site(request):
    deals = [
        {
            'title': 'Szorty kąpielowe',
            'price': f'{random()*20:.2f}',
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
        qs = (
            ScrapingTask.objects
            .filter(user=user)
            .order_by('favourite', 'title')
        )

        return qs


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
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return ScrapingJob.objects.filter(user=user).order_by('url')


class ScrapingJobDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ScrapingJob

    def test_func(self):
        return test_request_vs_object_user(self)


class ScrapingJobCreateView(LoginRequiredMixin, CreateView):
    model = ScrapingJob
    form_class = ScrapingJobForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ScrapingJobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ScrapingJob
    form_class = ScrapingJobForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return test_request_vs_object_user(self)


class ScrapingJobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ScrapingJob
    success_url = '/scraping-jobs/'

    def test_func(self):
        return test_request_vs_object_user(self)


class Diff(NamedTuple):
    data: str
    status: str


@login_required
def job_table(request):
    user = request.user

    all_jobs = ScrapingJob.objects.filter(user=user).order_by('url')

    paginator = Paginator(all_jobs, 20)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    context = {
        'is_paginated': True,
        'page_obj': jobs,
        'jobs': jobs,
    }

    return render(request, 'scraper/scrapingjob_table.html', context=context)


@login_required
def item_list(request):
    user = request.user

    all_items = Item.objects.filter(scraping_job__user=user)\
        .annotate(latest_state_update=Max('itemstate__date_found'))\
        .order_by('-latest_state_update').all()

    paginator = Paginator(all_items, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    items_data = []

    for item in items:
        last_two_states = item.itemstate_set.order_by('-date_found')[0:2]
        combined_keys = set()
        for state in last_two_states:
            data = state.data_as_dict()
            combined_keys |= set(k for k in data.keys() if data[k])
        combined_keys = sorted(combined_keys)

        if len(last_two_states) == 2:
            current_state, older_state = last_two_states
        elif len(last_two_states) == 1:
            current_state, older_state = last_two_states[0], None
        else:
            continue

        if older_state:
            older_date_found = older_state.date_found
        else:
            older_date_found = ''

        recent_history = {
            'current_date_found': current_state.date_found,
            'older_date_found': older_date_found,
            'rest': []
        }

        for key in combined_keys:
            current_value = current_state.data_as_dict().get(key, '')
            if older_state:
                older_value = older_state.data_as_dict().get(key, '')
            else:
                older_value = ''

            recent_history['rest'].append(
                {
                    'attribute': key,
                    'current': current_value,
                    'old': older_value
                }
            )

        items_data.append({
            'identifier': item.identifier,
            'url': item.url,
            'last_update': item.latest_state_update,
            'last_run': item.scraping_job.last_log.date_run,
            'last_run_result': item.scraping_job.last_log.result,
            'last_run_result_info': item.scraping_job.last_log.result_info,
            'recent_history': recent_history
        })

    context = {
        'is_paginated': True,
        'page_obj': items,
        'items_data': items_data
    }
    return render(request, 'scraper/item_list.html', context=context)


@login_required
def scraping_job_test_run(request, pk):
    scraping_job = get_object_or_404(ScrapingJob, pk=pk)
    task = yaml.safe_load(scraping_job.scraping_task.task)

    try:
        results, page_source = item_scraper.scrap(
            url=scraping_job.url,
            task=task,
            chromedriver_path=settings.SCRAPER_CHROMEDRIVER_PATH,
            user_agent=settings.SCRAPER_USER_AGENT
        )
    except ScrapTaskValidationError as exception:
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
