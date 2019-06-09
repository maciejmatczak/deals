from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import ScrapingTask

deals = [
    {
        'title': 'Super TSHIRT',
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
