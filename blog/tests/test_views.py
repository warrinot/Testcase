from django.test import TestCase, RequestFactory
from ..models import Post
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .. import views
from django.urls import reverse
from django.http import Http404
from django.test import Client


User = get_user_model()


class PostsTest(TestCase):
    ''' Test module for Posts '''

    def setUp(self):
        self.user = User.objects.create_user(
            email='lennon@thebeatles.com',
            username='john',
            password='johnpassword'
        )

    def test_post_create(self):
        post = Post.objects.create(title='Test title', text='Test text', blog=self.user.blog)
        self.assertTrue(post, 'Post creation error')


class BlogSubscribersTest(TestCase):

    def setUp(self):
        self.john = User.objects.create_user(
            email='lennon@thebeatles.com',
            username='john',
            password='johnpassword'
        )
        self.paul = User.objects.create_user(
            email='paul@thebeatles.com',
            username='paul',
            password='paulpassword'
        )
        self.ringo = User.objects.create_user(
            email='ringo@thebeatles.com',
            username='ringo',
            password='ringopassword'
        )

        self.user = authenticate(username='lennon@thebeatles.com', password='johnpassword')

    def test_manual_subscribe(self):
        subs_before = self.john.blog.subscriber.all()
        self.assertEqual(subs_before.count(), 0, 'Subs count is wrong')
        self.john.blog.subscriber.add(self.paul)
        subs_after = self.john.blog.subscriber.all()
        self.assertEqual(subs_after.count(), 1, 'Subs count is wrong')

        self.assertEqual(self.paul.blog.subscriber.all().count(), 0, 'Subs count is wrong')

    def test_manual_unsubscribe(self):
        # 0 subs
        subs_before = self.john.blog.subscriber.all()
        self.assertEqual(subs_before.count(), 0, 'Subs count is wrong')
        self.john.blog.subscriber.add(self.paul)
        # 1 sub
        subs_after = self.john.blog.subscriber.all()
        self.assertEqual(subs_after.count(), 1, 'Subs count is wrong')
        self.john.blog.subscriber.remove(self.paul)
        # 0 subs again
        subs_again = self.john.blog.subscriber.all()
        self.assertEqual(subs_again.count(), 0, 'Subs count is wrong')


class PersonalFeedViewTest(TestCase):
    '''Testing PersonalFeed view'''

    def setUp(self):
        self.john = User.objects.create_user(
            email='lennon@thebeatles.com',
            username='john',
            password='johnpassword'
        )
        self.paul = User.objects.create_user(
            email='paul@thebeatles.com',
            username='paul',
            password='paulpassword')
        self.factory = RequestFactory()

    def test_feed_shows_correct_posts(self):
        post_to_show = Post.objects.create(
            title='Test title', text='Text to show', blog=self.paul.blog)
        post_to_not_show = Post.objects.create(
            title='Test title 2', text='Text to not show', blog=self.john.blog)
        self.paul.blog.subscriber.add(self.john)

        request = self.factory.get(reverse('feed'))
        request.user = self.john
        response = views.personal_feed(request)
        self.assertIn(post_to_show.text.encode('utf-8'), response.content)
        self.assertNotIn(post_to_not_show.text.encode('utf-8'), response.content)


class PostDetailUpdateDeleteTest(TestCase):

    def setUp(self):
        self.john = User.objects.create_user(
            email='lennon@thebeatles.com',
            username='john',
            password='johnpassword'
        )
        self.paul = User.objects.create_user(
            email='paul@thebeatles.com',
            username='paul',
            password='paulpassword')
        self.draft_post = Post.objects.create(title='Test title',
                                              text='Test text',
                                              blog=self.john.blog, status='draft')
        self.published_post = Post.objects.create(title='Test title',
                                                  text='Test text',
                                                  blog=self.john.blog, status='published')

    def test_can_access_own_draft_post_detail(self):
        # user requests his own 'draft' post
        request = RequestFactory().get('post/')
        request.user = self.john
        view = views.PostDetailView()
        view.setup(request)
        view.kwargs = {'pk': self.draft_post.id}
        detail_object = view.get_object()
        self.assertEqual(detail_object, self.draft_post)

    def test_cant_access_anothers_draft_post_detail_fail(self):
        # paul tries to access john's 'draft' post
        request = RequestFactory().get('post/')
        request.user = self.paul
        view = views.PostDetailView()
        view.setup(request)
        view.kwargs = {'pk': self.draft_post.id}
        try:
            view.get_object()
        except Exception:
            pass
        self.assertRaises(Http404)

    def test_can_update_own_post(self):
        # john can update his own post
        request = RequestFactory().get('post/update')
        request.user = self.john
        view = views.PostUpdateView()
        view.setup(request)
        view.kwargs = {'pk': self.published_post.id}
        update_object = view.get_object()
        self.assertEqual(update_object, self.published_post)

    def test_cant_access_anothers_post_to_update(self):
        # paul tries to update john's post
        request = RequestFactory().get('post/update')
        request.user = self.paul
        view = views.PostUpdateView()
        view.setup(request)
        view.kwargs = {'pk': self.published_post.id}
        try:
            view.get_object()
        except Exception:
            pass
        self.assertRaises(Http404)

    def test_user_can_delete_own_post(self):
        # john tries to delete his own post
        request = RequestFactory().get('post/delete')
        request.user = self.john
        view = views.PostDeleteView()
        view.setup(request)
        view.kwargs = {'pk': self.published_post.id}
        response = view.get(request)
        self.assertContains(response, 'Вы уверены, что хотите удалить запись?')

    def test_user_cant_delete_anothers_post(self):
        # paul triest to delete john's post
        request = RequestFactory().get('post/delete')
        request.user = self.paul
        view = views.PostDeleteView()
        view.setup(request)
        view.kwargs = {'pk': self.published_post.id}
        try:
            view.get(request)
        except Exception:
            pass
        self.assertRaises(Http404)


class UserPostPageTest(TestCase):
    ''' Test module for user's page '''

    def setUp(self):
        self.john = User.objects.create_user(
            email='lennon@thebeatles.com',
            username='john',
            password='johnpassword'
        )
        self.paul = User.objects.create_user(
            email='paul@thebeatles.com',
            username='paul',
            password='paulpassword')
        self.draft_post_john = Post.objects.create(title='draft post john',
                                                   text='draft post john',
                                                   blog=self.john.blog, status='draft')
        self.published_post_john = Post.objects.create(title='published post john',
                                                       text='published post john',
                                                       blog=self.john.blog, status='published')
        self.published_post_paul = Post.objects.create(title='published post paul',
                                                       text='published post paul',
                                                       blog=self.paul.blog, status='published')

    def test_only_shows_published_by_user_posts(self):
        request = RequestFactory().get('blogs/')
        request.user = self.paul
        view = views.UserPostPage()
        view.setup(request)
        view.kwargs['blog'] = self.john.blog.id
        queryset = view.get_queryset()
        self.assertIn(self.published_post_john, queryset)
        self.assertNotIn(self.published_post_paul, queryset)
        self.assertNotIn(self.draft_post_john, queryset)

    def test_feed_shows_included_contextdata(self):
        request = RequestFactory().get('user/')
        request.user = self.john
        view = views.UserPostPage()
        view.setup(request)
        view.kwargs['blog'] = self.john.blog.id
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn('blog', context)
