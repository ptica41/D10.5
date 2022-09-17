from celery import shared_task
from datetime import timedelta, datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category

@shared_task
def new_post(id):
    post = Post.objects.get(pk=id)
    senders = []
    for category in post.category.all():
        for subscriber in category.subscribers.all():
            senders.append(subscriber.email)

    html_content = render_to_string('email.html', {'post': post})
    msg = EmailMultiAlternatives(
        subject=f'{post.head}',
        body='',
        from_email='skill41@yandex.ru',
        to=senders
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def recieve_mail():

    for category in Category.objects.all():
        posts = Post.objects.filter(time__gt=(datetime.now() - timedelta(days=7)), category=category.id)
        senders = []
        for subscriber in category.subscribers.all():
            senders.append(subscriber.email)
        html_content = render_to_string('email_week.html', {'posts': posts})
        msg = EmailMultiAlternatives(
            subject=f'Список свежих статей за неделю',
            body='',
            from_email='skill41@yandex.ru',
            to=senders
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()