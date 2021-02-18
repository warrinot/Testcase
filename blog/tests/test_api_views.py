import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post
from ..serializers import PostSerializer
from django.contrib.auth import get_user_model


User = get_user_model()
# Testing views
# протестить каждый CBV, подписку, отметки "прочитано".


# Testing Api
client = Client()


def create_test_user():
    new_user = User.objects.create(email='testemail@test.com',
                                   username='testuser', password='testpassword')
    return new_user


class GetAllPostsTest(TestCase):
    '''Test module for GET all Posts API'''

    def setUp(self):
        self.user = create_test_user()
        client.force_login(self.user)
        Post.objects.create(title='Test title',
                            text='Test text', blog=self.user.blog)
        Post.objects.create(title='Test title second',
                            text='Test text second', blog=self.user.blog)
        Post.objects.create(title='Test title third',
                            text='Test text third', blog=self.user.blog)
        Post.objects.create(title='Test title fourth',
                            text='Test text fourth', blog=self.user.blog)

    def test_get_all_posts(self):
        # get API response
        response = client.get(reverse('post-list'))
        # get data from db
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePostTest(TestCase):
    '''Test module for GET single Post API'''

    def setUp(self):
        self.user = create_test_user()
        client.force_login(self.user)
        self.post1 = Post.objects.create(
            title='Test title', text='Test text', blog=self.user.blog)
        self.post2 = Post.objects.create(
            title='Test title second', text='Test text second', blog=self.user.blog)
        self.post3 = Post.objects.create(title='Test title third',
                                         text='Test text third', blog=self.user.blog)
        self.post4 = Post.objects.create(
            title='Test title fourth', text='Test text fourth', blog=self.user.blog)

    def test_get_valid_single_post(self):
        response = client.get(
            reverse('post-detail', kwargs={'pk': self.post1.pk}))
        post = Post.objects.get(pk=self.post1.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_post(self):
        response = client.get(reverse('post-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPostTest(TestCase):

    def setUp(self):
        self.user = create_test_user()
        client.force_login(self.user)
        self.valid_payload = {
            'title': 'Test title',
            'text': 'Test text',
            'blog': self.user.blog.id
        }
        self.invalid_payload = {
            'title': '',
            'text': 'Test text',
            'blog': self.user.blog.id
        }

    def test_create_valid_post(self):
        response = client.post(reverse('post-list'), data=json.dumps(
            self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_post(self):
        response = client.post(reverse('post-list'), data=json.dumps(
            self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePostTest(TestCase):
    ''' Test module for updating an existing post '''

    def setUp(self):
        self.user = create_test_user()
        client.force_login(self.user)
        self.post1 = Post.objects.create(
            title='Test title', text='Test text', blog=self.user.blog)
        self.post2 = Post.objects.create(
            title='Test title second', text='Test text second', blog=self.user.blog)
        self.valid_payload = {
            'title': 'Test title updated',
            'text': 'Test text updated',
            'blog': self.user.blog.id
        }
        self.invalid_payload = {
            'title': 1,
            'text': ['list instead of text'],
            'blog': self.user.blog.id
        }

    def test_valid_update_post(self):
        response = client.put(reverse('post-detail', kwargs={'pk': self.post2.pk}),
                              data=json.dumps(self.valid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_post(self):
        response = client.put(reverse('post-detail', args=(self.post2.pk, )),
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePostTest(TestCase):
    ''' Test module for deleting an existing post '''

    def setUp(self):
        self.user = create_test_user()
        client.force_login(self.user)
        self.post1 = Post.objects.create(
            title='Test title', text='Test text', blog=self.user.blog)
        self.post2 = Post.objects.create(
            title='Test title second', text='Test text second', blog=self.user.blog)

    def test_valid_delete_post(self):
        response = client.delete(
            reverse('post-detail', kwargs={'pk': self.post2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        response = client.delete(reverse('post-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
