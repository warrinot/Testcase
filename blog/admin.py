from django.contrib import admin
from .models import Blog, Post
# Register your models here.


class AdminBlog(admin.ModelAdmin):
    filter_horizontal = ['subscriber']


class AdminPost(admin.ModelAdmin):
    list_display = ['title', 'date_added', 'blog', 'status', 'status_changed', ]
    filter_horizontal = ['seen_by']


admin.site.register(Post, AdminPost)
admin.site.register(Blog, AdminBlog)
