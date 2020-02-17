from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from textwrap import dedent

from .models import ItemState


@receiver(post_save, sender=ItemState)
def new_state_sends_mail(sender, instance, **kwargs):
    # TODO: create proper templates
    # msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
    # msg_html = render_to_string('templates/email.html', {'some_params': some_params})
    user = instance.item.user
    date_found = instance.date_found
    data = instance.data

    msg_plain = dedent(f'''\
Hi {user}!

Found awesome stuff Today:

{instance.item.identifier}

{instance.item.url}

{data}
    ''')

    msg_html = dedent(f'''\
Hi {user}!

Found awesome stuff Today:

{instance.item.identifier}

<img src="{"https://scraper.ellox.science/media" + str(instance.item.image)}" alt="{instance.item.identifier}"/>

<a href="{instance.item.url}">Check it out!</a>

{data}
    ''')

    send_mail(
        f'Scrapped new items: {date_found}',
        msg_plain,
        'noreply@scraper.ellox.science',
        [user.email],
        html_message=msg_html
    )
