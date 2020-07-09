from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UsersList

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_field_name='posts/'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('users_list/', UsersList.as_view(), name='users_list'),

]
