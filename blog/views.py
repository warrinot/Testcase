from django.urls import reverse_lazy
from .models import Post, Blog
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


User = get_user_model()
PAGINATE = 15


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(status='published').order_by('-date_added')
    paginate_by = PAGINATE


def personal_feed(request):

    subbed_on = Blog.objects.filter(subscriber=request.user)
    if subbed_on:
        queryset = Post.objects.all()
        for blog in subbed_on:
            queryset = queryset.filter(blog__subscriber=request.user)
        queryset = queryset.exclude(seen_by=request.user).order_by('-date_added')
    else:
        queryset = Post.objects.none()

    paginator = Paginator(queryset, PAGINATE)
    is_paginated = paginator.num_pages > 1
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'all_posts': posts, 'page': page, 'is_paginated': is_paginated}
    return render(request, 'blog/feed.html', context)


class PostDraftView(ListView):
    paginate_by = PAGINATE

    def get_queryset(self):
        return Post.objects.filter(blog=self.request.user.blog).filter(
            status='draft').order_by('-date_added')


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        ''' Make sure other users can't see draft posts of another user'''
        obj = super(PostDetailView, self).get_object()
        if not obj.blog == self.request.user.blog and obj.status == 'draft':
            raise Http404
        return obj


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'text', 'status']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.blog = self.request.user.blog
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text', 'status']
    success_url = reverse_lazy('post_list')
    template_name = 'blog/post_update.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PostUpdateView, self).get_object()
        if not obj.blog == self.request.user.blog:
            if not self.request.user.is_staff:
                raise Http404
        return obj


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PostDeleteView, self).get_object()
        if not obj.blog == self.request.user.blog:
            if not self.request.user.is_staff:
                raise Http404
        return obj


class UserPostPage(ListView):
    template_name = 'blog/user_page.html'

    def get_queryset(self):
        self.owner = get_object_or_404(User, username=self.kwargs['user'])
        return Post.objects.filter(blog__user=self.owner).filter(
            status='published').order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = get_object_or_404(User, username=self.kwargs['user'])
        owner = context['owner']
        context['blog'] = get_object_or_404(Blog, user=owner)
        return context


def user_post_page(request, user_id):
    posts = Post.objects.filter(blog__user__id=user_id)
    return render(request, 'blog/user_page.html', {'object_list': posts})


def add_sub_ajax(request):
    if request.is_ajax():
        blog_author = int(request.POST['author_id'])
        targeted_blog = Blog.objects.get(user=blog_author)
        subs = targeted_blog.subscriber.all()
        if request.user not in subs:
            targeted_blog.subscriber.add(request.user)
        else:
            targeted_blog.subscriber.remove(request.user)
        subbed = request.user in subs

        return JsonResponse({'subbed': subbed})


def make_post_seen(request, post_id):
    target_post = Post.objects.get(id=post_id)
    target_post.seen_by.add(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def test_auth(request):
    user = authenticate(username='test@test.com', password='12345678aA')
    login(request, user)
    return redirect('post_list')
