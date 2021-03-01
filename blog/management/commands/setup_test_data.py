import random
from django.contrib.auth import get_user_model

from django.db import transaction
from django.core.management.base import BaseCommand

from blog.models import Post
from blog.factories import (
    UserFactory,
    PostFactory,
)
User = get_user_model()
NUM_USERS = 50
NUM_POSTS = 150


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Post]
        for m in models:
            mod = m.objects.all()
            if m == User:
                mod = mod.exclude(email='warrinot@gmail.com')
                mod = mod.exclude(email='ahhipiro@gmail.com')
                mod = mod.exclude(email='test@test.com')

            mod.delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        people = []
        for _ in range(NUM_USERS):
            person = UserFactory()
            people.append(person)

        # Create all the posts
        for _ in range(NUM_POSTS):
            poster = random.choice(people)
            PostFactory(
                blog=poster.blog)
