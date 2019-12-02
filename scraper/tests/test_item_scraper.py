from pytest import raises
from pathlib import Path
import yaml
from io import StringIO
from textwrap import dedent

from scraper.item_scraper.item_scraper import parse
from scraper.item_scraper.validators import (
    ValidationError,
    validate_css_selector,
    validate_file_path,
    validate_task,
)


CACHE_DIR = Path(__file__).parent / 'data' / 'cache_dir'


def test_css_selector_validator():
    with raises(ValidationError):
        validate_css_selector('|_|_')


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


def test_parse():
    task = {
        'item': 'div.card',
        'extract': {
            'image': 'img.card-img-top|src',
            'title': '.card-title|text',
            'description': 'p.card-text|text',
            'nonExistingField': 'p.blabla|text',
        }
    }

    page_source = (CACHE_DIR / 'https___deals_ellox_science_').read_text()

    data = parse(page_source, task)

    assert data
    assert len(data) == 8
    for item in data:
        assert item['image'] == '/static/generic.jpg'
        assert 'Super' in item['title']
        assert '99' in item['description']
        assert item['nonExistingField'] is None
