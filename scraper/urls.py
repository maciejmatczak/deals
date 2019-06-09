from django.urls import path

from .views import (home, ScrapingTaskListView, ScrapingTaskDetailView,
                    ScrapingTaskCreateView, ScrapingTaskUpdateView, ScrapingTaskDeleteView)

urlpatterns = [
    path('', home, name='scraper-home'),
    path('scraping-tasks/', ScrapingTaskListView.as_view(), name='scrapingtasks'),
    path('scraping-task/<int:pk>/', ScrapingTaskDetailView.as_view(), name='scrapingtask-detail'),
    path('scraping-task/new/', ScrapingTaskCreateView.as_view(), name='scrapingtask-create'),
    path('scraping-task/<int:pk>/update/', ScrapingTaskUpdateView.as_view(), name='scrapingtask-update'),
    path('scraping-task/<int:pk>/delete/', ScrapingTaskDeleteView.as_view(), name='scrapingtask-delete'),
]
