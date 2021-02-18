from rest_framework import serializers
from .models import Post, Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'user', 'posts']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date_added', 'blog']
        depth = 0
