from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import string
from pathlib import Path
from urllib.request import Request, urlopen, HTTPError


def format_filename(s):
    valid_chars = '-_() %s%s' % (string.ascii_letters, string.digits)
    filename = ''.join(c if c in valid_chars else '_' for c in s)
    filename = filename.replace(' ', '_')

    return filename


def download_page(url, chromedriver_path, cache_dir=None, use_cache=False,
                  endless_page=True, user_agent=None):
    page_source = None

    if cache_dir:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)

        file_path = cache_dir / f'{format_filename(url)}.html'

        if use_cache:
            try:
                with file_path.open('r', encoding='utf-8') as f:
                    page_source = f.read()
            except IOError:
                pass

    if not page_source:
        request = Request(
            url,
            data=None,
            headers={
                'User-Agent': user_agent
            }
        )
        urlopen(url)

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('--disable-gui')

        if user_agent:
            options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(chromedriver_path, options=options)
        driver.implicitly_wait(1)

        driver.get(url)

        if endless_page:
            for _ in range(5):
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                driver.implicitly_wait(2)
        page_source = driver.page_source

        if cache_dir:
            with file_path.open('w', encoding='utf-8') as f:
                f.write(page_source)

    return page_source
