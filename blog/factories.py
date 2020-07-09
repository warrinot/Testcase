import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name", locale='ru_RU')
    email = factory.Faker("email")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
    title = factory.Faker('sentence', nb_words=5, variable_nb_words=True, locale='ru_RU')
    text = factory.Faker('paragraph', nb_sentences=4, variable_nb_sentences=True, locale='ru_RU')
