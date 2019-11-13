from django.urls import path

from .views import (home, ScrapingJobListView, ScrapingJobDetailView,
                    ScrapingJobCreateView, ScrapingJobUpdateView,
                    ScrapingJobDeleteView, scraping_job_test_run, test_site,
                    ScrapingTaskListView, ScrapingTaskDetailView,
                    ScrapingTaskCreateView, ScrapingTaskUpdateView,
                    ScrapingTaskDeleteView, ItemListView)

urlpatterns = [
    path('', home, name='scraper-home'),
    path('test-site/', test_site, name='scraper-testsite'),
    path('scraping-jobs/', ScrapingJobListView.as_view(), name='scrapingjobs'),
    path('scraping-job/<int:pk>/', ScrapingJobDetailView.as_view(),
         name='scrapingjob-detail'),
    path('scraping-job/<int:pk>/testrun/',
         scraping_job_test_run, name='scrapingjob-testrun'),
    path('scraping-job/new/', ScrapingJobCreateView.as_view(),
         name='scrapingjob-create'),
    path('scraping-job/<int:pk>/update/',
         ScrapingJobUpdateView.as_view(), name='scrapingjob-update'),
    path('scraping-job/<int:pk>/delete/',
         ScrapingJobDeleteView.as_view(), name='scrapingjob-delete'),
    path('scraping-tasks/', ScrapingTaskListView.as_view(), name='scrapingtasks'),
    path('scraping-task/<int:pk>/', ScrapingTaskDetailView.as_view(),
         name='scrapingtask-detail'),
    path('scraping-task/<int:pk>/', ScrapingTaskDetailView.as_view(),
         name='scrapingtask-testrun'),
    path('scraping-task/new/', ScrapingTaskCreateView.as_view(),
         name='scrapingtask-create'),
    path('scraping-task/<int:pk>/update/',
         ScrapingTaskUpdateView.as_view(), name='scrapingtask-update'),
    path('scraping-task/<int:pk>/delete/',
         ScrapingTaskDeleteView.as_view(), name='scrapingtask-delete'),
    path('scrapped-items/',
         ItemListView.as_view(), name='scrappeditems'),
]
