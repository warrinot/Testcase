from django.test import TestCase
from ..models import Post, Blog
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()


class BlogAndUserCreationTest(TestCase):
    ''' Test module for blog and user creation'''

    def setUp(self):
        self.john = User.objects.create_user(
            email='lennon@thebeatles.com',
            username='john',
            password='johnpassword'
        )

    def test_blog_creation(self):
        self.assertTrue(self.john.blog, 'Blog creation error')

    def test_user(self):
        self.user = authenticate(username='lennon@thebeatles.com', password='johnpassword')
        self.assertTrue(self.user.is_active, 'User login error')
        self.assertTrue(self.user.is_authenticated, 'User login error')


class PostModelTest(TestCase):
    '''Test module for Post model '''

    def setUp(self):
        self.user = User.objects.create(email='testemail@test.com', username='testuser')

    def test_posting_success(self):
        first_post = Post.objects.create(title='Test post', text='Test text', blog=self.user.blog)
        second_post = Post.objects.create(title='Second test post',
                                          text='Text for second test', blog=self.user.blog)
        self.assertEqual(first_post.title, 'Test post')
        self.assertEqual(second_post.title, 'Second test post')
        self.assertEqual(first_post.text, 'Test text')
        self.assertEqual(second_post.text, 'Text for second test')

    def test_post_str(self):
        post_totest = Post.objects.create(title='Test post', text='Test text', blog=self.user.blog)
        self.assertEqual(post_totest.__str__(), post_totest.title)

    def test_post_statuschanged_correctly_changes_on_post_save(self):
        # creating post with status == 'draft'
        tested_post = Post.objects.create(title='Test post',
                                          text='Test text',
                                          blog=self.user.blog,
                                          status='draft')
        # test that status was not changed
        self.assertFalse(tested_post.status_changed)
        # changing post status from 'draft' to 'published'
        tested_post.status = 'published'
        tested_post.save()
        self.assertEqual(tested_post.status_changed, True)


class BlogModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='testemail@test.com', username='testuser')

    def test_blog_str(self):
        blog = Blog.objects.first()
        self.assertEqual(blog.__str__(), "testuser's blog")
