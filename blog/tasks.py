from testcase.celery import app
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site


@app.task
def post_created(post_url, blog_name, recepients):
    domain = str(get_current_site(None))
    subject = f'Новый пост от { blog_name }'
    message = f'Новый пост в блоге на который вы подписаны!  { domain + post_url }'
    mail_sent = send_mail(subject, message, 'admin@bookstore.com', [recepients])
    return mail_sent
