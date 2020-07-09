from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from .views import UsersList


User = get_user_model()


class UsersManagersTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class UsersListViewTest(TestCase):

    def test_get_queryset_returns_correct(self):
        first_user = User.objects.create_user(email='first_user@user.com', password='foo')
        second_user = User.objects.create_user(email='second_user@user.com', password='foo')
        third_user = User.objects.create_user(email='third_user@user.com', password='foo')

        request = RequestFactory().get('users/users_list/')
        view = UsersList()
        view.setup(request)

        queryset = view.get_queryset()
        self.assertIn(first_user, queryset)
        self.assertIn(second_user, queryset)
        self.assertIn(third_user, queryset)
