from django.urls import path

from .views import (job_table, ScrapingJobListView, ScrapingJobDetailView,
                    ScrapingJobCreateView, ScrapingJobUpdateView,
                    ScrapingJobDeleteView, scraping_job_test_run, test_site,
                    ScrapingTaskListView, ScrapingTaskDetailView,
                    ScrapingTaskCreateView, ScrapingTaskUpdateView,
                    ScrapingTaskDeleteView, item_list, item_image)

urlpatterns = [
    path('', item_list, name='scrapeditems'),
    path('item/<int:pk>/image/', item_image, name='item-image'),
    path('test-site/', test_site, name='scraper-testsite'),
    path('jobs/', job_table, name='scrapingjobs'),
    path('job/<int:pk>/', ScrapingJobDetailView.as_view(),
         name='scrapingjob-detail'),
    path('job/<int:pk>/testrun/',
         scraping_job_test_run, name='scrapingjob-testrun'),
    path('job/new/', ScrapingJobCreateView.as_view(),
         name='scrapingjob-create'),
    path('job/<int:pk>/update/',
         ScrapingJobUpdateView.as_view(), name='scrapingjob-update'),
    path('job/<int:pk>/delete/',
         ScrapingJobDeleteView.as_view(), name='scrapingjob-delete'),
    path('tasks/', ScrapingTaskListView.as_view(), name='scrapingtasks'),
    path('task/<int:pk>/', ScrapingTaskDetailView.as_view(),
         name='scrapingtask-detail'),
    path('task/<int:pk>/', ScrapingTaskDetailView.as_view(),
         name='scrapingtask-testrun'),
    path('task/new/', ScrapingTaskCreateView.as_view(),
         name='scrapingtask-create'),
    path('task/<int:pk>/update/',
         ScrapingTaskUpdateView.as_view(), name='scrapingtask-update'),
    path('task/<int:pk>/delete/',
         ScrapingTaskDeleteView.as_view(), name='scrapingtask-delete')
]
