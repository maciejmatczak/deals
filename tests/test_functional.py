import pytest
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.auth.hashers import make_password
from django.urls import reverse


def test_home_page(live_server, browser):
    # Open the home page
    browser.get(live_server.url)

    assert 'Deals' in browser.title

    browser.find_element_by_partial_link_text("jobs").click()


@pytest.mark.django_db
def test_standard_scenario(live_server, browser, user_factory,
                           scraping_job_factory, scraping_task_factory):
    # let's have two users
    user1 = user_factory.create(password=make_password('1234'))
    user2 = user_factory.create(password=make_password('5678'))

    # user1 creates some tasks, as well as jobs - different task per job
    task11 = scraping_task_factory.create(user=user1)
    task12 = scraping_task_factory.create(user=user1)

    job11 = scraping_job_factory.create(user=user1, scraping_task=task11)
    job12 = scraping_job_factory.create(user=user1, scraping_task=task12)

    # user 2 will have one task and would use it for 2 jobs
    task2 = scraping_task_factory.create(user=user2)
    job21 = scraping_job_factory.create(user=user2, scraping_task=task2)
    job22 = scraping_job_factory.create(user=user2, scraping_task=task2)

    # Open the home page and log in as user1
    browser.get(live_server.url)

    # user is not yet logged in, so trying to view jobs should show login view
    browser.find_element_by_partial_link_text("jobs").click()
    browser.find_element_by_name('username').send_keys(user1.username)
    browser.find_element_by_name('password').send_keys('1234')
    browser.find_element_by_css_selector("button[type='submit']").click()

    browser.find_element_by_partial_link_text("jobs").click()

    # user1 should se only 2 jobs
    jobs_divs = browser.find_elements_by_css_selector('div.entry-section')
    assert len(jobs_divs) == 2

    # but let's double check if detail view of the other one gives an error
    browser.get(live_server.url + reverse('scrapingjob-detail', args=[job21.pk]))
    assert '403' in browser.page_source

    # let's assume we just can find both task data within the detail
    # page
    browser.get(live_server.url + reverse('scrapingjob-detail', args=[job11.pk]))
    assert task11.task in browser.find_element_by_tag_name('body').text,\
        browser.find_element_by_tag_name('body').text
    browser.get(live_server.url + reverse('scrapingjob-detail', args=[job12 .pk]))
    assert task12.task in browser.find_element_by_tag_name('body').text,\
        browser.find_element_by_tag_name('body').text

    # we should be able to change second job to task11
    browser.get(live_server.url + reverse('scrapingjobs'))
    browser.find_element_by_partial_link_text(job12.url).click()
    browser.find_element_by_partial_link_text('Update').click()
    for option in browser.find_elements_by_css_selector(
        "select[name='scraping_task'] option"
    ):
        if task11.title in option.text:

            option.click()
            break
    else:
        pytest.fail('Did not found task to click!')
    browser.find_element_by_css_selector('button[type=submit').click()

    # and after all this change we and with following:
    # job11 still have task11
    browser.get(live_server.url + reverse('scrapingjob-detail', args=[job11.pk]))
    assert task11.task in browser.find_element_by_tag_name('body').text,\
        browser.find_element_by_tag_name('body').text
    # but job12 should have task11
    browser.get(live_server.url + reverse('scrapingjob-detail', args=[job12.pk]))
    assert task12.task not in browser.find_element_by_tag_name('body').text,\
        browser.find_element_by_tag_name('body').text
