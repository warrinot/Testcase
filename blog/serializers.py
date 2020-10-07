from rest_framework import serializers
from .models import Post, Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['id', 'user']
        extra_kwargs = {
            'user': {'validators': []},
        }

class PostSerializer(serializers.ModelSerializer):
    # blog = BlogSerializer()
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date_added', 'blog']