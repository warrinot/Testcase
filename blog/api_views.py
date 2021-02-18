from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import serializers
from .serializers import PostSerializer, BlogSerializer
from .models import Post, Blog


class PostApiViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('blog__user').order_by('date_added')

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class BlogApiViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()

    serializer_class = BlogSerializer
