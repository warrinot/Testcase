from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from blog import api_views
from django.conf import settings


router = routers.DefaultRouter()
router.register(r'posts', api_views.PostApiViewSet)
router.register(r'blogs', api_views.BlogApiViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls))

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
