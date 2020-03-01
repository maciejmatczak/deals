from lxml import html
from io import StringIO
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen, HTTPError

# from .page_downloader import download_page, download_and_scrap_page
from .validators import validate_task, validate_file_path, ValidationError


SPACES = re.compile(r'\s')


def scrap(url, task, chromedriver_path, endless_page=True, user_agent=None):
    validate_task(task)

    try:
        validate_file_path(chromedriver_path)
    except ValidationError as error:
        raise ValidationError(
            f'chromedriver was not found!'
            f'{error}'
        )

    check_page_accessibility(url, user_agent=user_agent)

    driver = setup_chrome_driver(chromedriver_path, user_agent)

    driver.get(url)
    driver.implicitly_wait(1)

    if endless_page:
        for _ in range(5):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1)

    page_source = driver.page_source

    data = parse(driver, task)

    return data, page_source


def check_page_accessibility(url, user_agent=None):
    # checking up before real run if page exists at all and is accessible
    if user_agent:
        header = {
            'User-Agent': user_agent
        }
    else:
        header = {}

    request = Request(
        url,
        data=None,
        headers=header
    )

    urlopen(request)


def setup_chrome_driver(chromedriver_path, user_agent):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-gui')

    if user_agent:
        options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(chromedriver_path, options=options)

    return driver


SPACES = re.compile(r'\s')


def parse(driver, task):
    data = []
    for item in driver.find_elements_by_css_selector(task['item']):

        sub_data = {}

        for field, expr_method in task['extract'].items():
            expr, method = expr_method.split('|')
            r = item.find_elements_by_css_selector(expr)

            if len(r) > 0:
                if method == 'text':
                    # text = r[0].text_content()
                    text = ' '.join(r.text for r in r)
                    cleaned_text = ' '.join(
                        el for el in SPACES.split(text) if el)

                    sub_data[field] = cleaned_text
                elif method == 'screenshot':
                    driver.execute_script(
                        '''
                            const elementRect = arguments[0].getBoundingClientRect();
                            const scrollTopOfElement = elementRect.top + elementRect.height / 2;
                            const scrollY = scrollTopOfElement - (window.innerHeight / 2);
                            window.scrollTo(0, scrollY);
                        ''',
                        r[0])
                    sub_data[field] = r[0].screenshot_as_png
                else:
                    sub_data[field] = r[0].get_attribute(method)
            else:
                sub_data[field] = None

        if any(sub_data.values()):
            data.append(sub_data)

    return data
