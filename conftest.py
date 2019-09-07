from django.conf import settings
import os
import pytest
from pytest_factoryboy import register
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from users.factories import UserFactory
from scraper.factories import ScrapingTaskFactory, ScrapingJobFactory


register(UserFactory)
register(ScrapingTaskFactory)
register(ScrapingJobFactory)


@pytest.fixture(scope='module')
def browser(request):
    options = Options()
    options.add_argument('--headless')

    browser_ = webdriver.Chrome(settings.SCRAPER_CHROMEDRIVER_PATH, options=options)

    yield browser_

    browser_.quit()
