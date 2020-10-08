from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


'''TODO:
    Async function of sending mails
'''


User = get_user_model()
STATUS_CHOICES = (
    ('published', 'Опубликовать'),
    ('draft', 'Черновик'),
)


class Blog(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='blog')
    subscriber = models.ManyToManyField(
        User, related_name='subscriber', blank=True)

    def __str__(self):
        return str(self.name) + '\'s blog'


class Post(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, verbose_name=('Заголовок'))
    text = models.TextField(verbose_name=('Текст'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    seen_by = models.ManyToManyField(User, related_name='seen', blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published', verbose_name=('Статус'))
    status_changed = models.BooleanField(default=False)
    __original_status = None

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.status == 'published' and self.__original_status == 'draft':
            self.status_changed = True
        else:
            pass
        super(Post, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status


@receiver(post_save, sender=User, dispatch_uid='user_created')
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        blog = Blog.objects.create(name=instance.username, user=instance)
        blog.save()


# @receiver(post_save, sender=Post, dispatch_uid='post_created')
# def send_email(sender, instance, created, **kwargs):
#     if instance.status == 'published':
#         subscribers = instance.blog.subscriber.all()
#         senders_emails = []
#         for sub in subscribers:
#             senders_emails.append(str(sub.email))

#         senderr = "Blog site"
#         link = f'http://127.0.0.1:8000/post/{instance.pk}'
#         if created:  # make sure it is new post and not edited.
#             send_mail(
#                 f'New post at {instance.blog}!',
#                 '',
#                 f'{senderr}',
#                 senders_emails,
#                 html_message=f'Link: \n <a href={link}>New post</a>')
#         else:
#             if instance.status_changed:
#                 send_mail(
#                     f'New post at {instance.blog}!!',
#                     '',
#                     f'{senderr}',
#                     senders_emails,
#                     html_message=f'Link: \n <a href={link}>New post</a>')
