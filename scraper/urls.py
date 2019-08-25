from django.urls import path

from .views import (home, ScrapingJobListView, ScrapingJobDetailView,
                    ScrapingJobCreateView, ScrapingJobUpdateView,
                    ScrapingJobDeleteView, scraping_job_test_run, test_site)

urlpatterns = [
    path('', home, name='scraper-home'),
    path('test-site/', test_site, name='scraper-testsite'),
    path('scraping-tasks/', ScrapingJobListView.as_view(), name='scrapingjobs'),
    path('scraping-task/<int:pk>/', ScrapingJobDetailView.as_view(), name='scrapingjob-detail'),
    path('scraping-task/testrun/<int:pk>/', scraping_job_test_run, name='scrapingjob-testrun'),
    path('scraping-task/new/', ScrapingJobCreateView.as_view(), name='scrapingjob-create'),
    path('scraping-task/<int:pk>/update/', ScrapingJobUpdateView.as_view(), name='scrapingjob-update'),
    path('scraping-task/<int:pk>/delete/', ScrapingJobDeleteView.as_view(), name='scrapingjob-delete'),
]
