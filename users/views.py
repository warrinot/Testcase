from django.views.generic import ListView
from blog.models import Blog


class UsersList(ListView):
    template_name = 'users/users_list.html'

    def get_queryset(self):
        queryset = Blog.objects.all().select_related('user') \
            .prefetch_related('subscriber').order_by('user')
        return queryset
