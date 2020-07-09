from django.contrib.auth import get_user_model
from django.views.generic import ListView


class UsersList(ListView):
    template_name = 'users/users_list.html'

    def get_queryset(self):
        return get_user_model().objects.all().order_by('username')
