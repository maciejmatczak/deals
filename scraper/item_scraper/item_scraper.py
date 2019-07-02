from lxml import html
from io import StringIO
import re

from .page_downloader import download_page
from .validators import validate_task, validate_file_path


SPACES = re.compile(r'\s')


def scrap(url, task, chromedriver_path, cache_dir=None, use_cache=False, endless_page=True):
    validate_task(task)
    validate_file_path(chromedriver_path)

    page_source = download_page(
        url,
        chromedriver_path,
        cache_dir=cache_dir,
        use_cache=use_cache,
        endless_page=endless_page,
    )

    data = parse(page_source, task)

    return data


def parse(page_source, task):
    # htmlparser = etree.HTMLParser()
    # tree = etree.parse(StringIO(page_source), htmlparser)
    tree = html.parse(StringIO(page_source))

    data = []
    for item in tree.getroot().cssselect(task['item']):
        # print('\n\nNew Item:')
        # print(etree.tostring(item, pretty_print=True, method='html', encoding='unicode'))
        sub_data = {}

        for field, expr_method in task['extract'].items():
            expr, method = expr_method.split('|')
            r = item.cssselect(expr)

            if len(r) > 0:
                if method == 'text':
                    # text = r[0].text_content()
                    text = ' '.join(r.text_content() for r in r)
                    cleaned_text = ' '.join(el for el in SPACES.split(text) if el)

                    sub_data[field] = cleaned_text
                else:
                    sub_data[field] = r[0].attrib.get(method)
            else:
                sub_data[field] = None

        if any(sub_data.values()):
            data.append(sub_data)

    return data
