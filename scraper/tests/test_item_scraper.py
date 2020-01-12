from pytest import raises
from pathlib import Path
import yaml
from io import StringIO
from textwrap import dedent

from django.conf import settings

from scraper.item_scraper.item_scraper import scrap
from scraper.item_scraper.validators import (
    ValidationError,
    validate_css_selector,
    validate_file_path,
    validate_task,
)


CACHE_DIR = Path(__file__).parent / 'data' / 'cache_dir'


def test_css_selector_validator():
    with raises(ValidationError):
        validate_css_selector('|_|sdaf;;_')


def test_file_path_validator(tmp_path):
    p = tmp_path / 'some_file.txt'
    p.touch()

    with raises(ValidationError):
        validate_file_path('|_|_')
    validate_file_path(p)
    validate_file_path(str(p))


def test_task_validator():
    with raises(ValidationError):
        task = yaml.safe_load(StringIO(dedent('''\
            item: some.item yielder | text
            extract:
              image: img.card-img-top|src
        ''')))

        validate_task(task)


def test_scrap(live_server):
    # adding ugly dependency to launched django app, testing on test-site,
    # since scrapper is selenium only

    task = yaml.safe_load(StringIO(dedent('''\
        item: div.card
        extract:
            identifier: .card-title|text
            image: img.card-img-top|src
            image2: img.card-img-top|screenshot
            title: .card-title|text
            description: p.card-text|text
            nonExistingField: p.blabla|text
    ''')))

    data, page_source = scrap(
        f'{live_server.url}/test-site', task,
        settings.SCRAPER_CHROMEDRIVER_PATH,
        endless_page=False)

    assert data
    assert len(data) == 8, page_source

    item = data[1]
    assert item['image'].endswith('/static/generic.jpg')
    assert 'Super' in item['title']
    assert '99' in item['description']
    assert item['nonExistingField'] is None
