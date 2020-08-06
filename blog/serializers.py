from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # possible to make it like this instead of using method
    # blog = CustomBlogSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date_added', 'date_changed', 'blog']
        depth = 1
