from cssselect import GenericTranslator, SelectorError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from pathlib import Path


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_url(url):
    validate = URLValidator(schemes=('http', 'https'))

    try:
        validate(url)
    except DjangoValidationError as exception:
        raise ValidationError(str(exception.message))


def validate_css_selector(selector):
    try:
        GenericTranslator().css_to_xpath(selector)
    except SelectorError as exception:
        raise ValidationError(
            f'For css selector "{selector}" exception was raised "{exception}"'
        )


def validate_task(task):
    for field in ('item', 'extract'):
        if field not in task:
            raise ValidationError(f'Field "{field}" not in task')

    for selector_extractor in task['extract'].values():
        if selector_extractor.count('|') == 0:
            raise ValidationError(
                f'Pipe "|" missing in "{selector_extractor}", no way to'
                f'distunguish selector from extractor'
            )
        elif selector_extractor.count('|') > 1:
            raise ValidationError(
                f'Only one pipe "|" allowed in selector-extractor: '
                f'"{selector_extractor}"'
            )


def validate_file_path(path):
    p = Path(path)
    if not (p.exists() and p.is_file()):
        raise ValidationError(f'File "{path}" does not exist')
