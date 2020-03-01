from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from textwrap import dedent

from .models import ItemState


@receiver(post_save, sender=ItemState)
def new_state_sends_mail(sender, instance, **kwargs):
    user = instance.item.user
    date_found = instance.date_found
    data = instance.data

    recent_history = instance.item.recent_history()

    msg_plain = dedent(f'''\
Hi {user}!

Found awesome stuff Today:

{instance.item.identifier}

{instance.item.url}

{data}
    ''')

    try:
        site_url = settings.ALLOWED_HOSTS[0]
    except IndexError:
        site_url = ''

    html_template = get_template('scraper/email_new_item.html')
    html_message = html_template.render(
        context={
            'user': user,
            'item': instance.item,
            'recent_history': recent_history,
            'site_url': site_url,
            'data': data
        }
    )

    send_mail(
        f'Scrapped new items: {date_found}',
        msg_plain,
        'Scraper <noreply@scraper.ellox.science>',
        [user.email],
        html_message=html_message
    )
