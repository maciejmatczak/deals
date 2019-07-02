from django.urls import path

from .views import (home, ScrapingTaskListView, ScrapingTaskDetailView,
                    ScrapingTaskCreateView, ScrapingTaskUpdateView,
                    ScrapingTaskDeleteView, scraping_task_test_run, test_site)

urlpatterns = [
    path('', home, name='scraper-home'),
    path('test-site/', test_site, name='scraper-testsite'),
    path('scraping-tasks/', ScrapingTaskListView.as_view(), name='scrapingtasks'),
    path('scraping-task/<int:pk>/', ScrapingTaskDetailView.as_view(), name='scrapingtask-detail'),
    path('scraping-task/testrun/<int:pk>/', scraping_task_test_run, name='scrapingtask-testrun'),
    path('scraping-task/new/', ScrapingTaskCreateView.as_view(), name='scrapingtask-create'),
    path('scraping-task/<int:pk>/update/', ScrapingTaskUpdateView.as_view(), name='scrapingtask-update'),
    path('scraping-task/<int:pk>/delete/', ScrapingTaskDeleteView.as_view(), name='scrapingtask-delete'),
]
