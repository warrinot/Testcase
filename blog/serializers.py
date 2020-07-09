from rest_framework import serializers
from .models import Post, Blog


class CustomBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['__str__']


class PostSerializer(serializers.ModelSerializer):
    # possible to make it like this instead of using method
    # owner = CustomBlogSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'date_added', 'date_changed', 'blog']

    def to_representation(self, instance):
        self.fields['blog'] = CustomBlogSerializer(read_only=True)
        return super(PostSerializer, self).to_representation(instance)
