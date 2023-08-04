from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from blog.forms import PostForm, CommentForm, UserForm
from blog.models import Category, Post, Comment

from blogicum.settings import PAGINATOR_VALUE


def index(request):
    template = 'blog/index.html'
    post_list = (
        Post.objects.published_posts()
        .select_related('category', 'location', 'author')
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    paginator = Paginator(post_list, PAGINATOR_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.objects.all(), pk=id)
    if not post.is_published and request.user != post.author:
        raise Http404
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.all(),
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category,
                                 slug=category_slug,
                                 is_published=True
                                 )
    post_list = category.posts.published_posts().order_by('-pub_date')
    paginator = Paginator(post_list, PAGINATOR_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


def user_profile(request, user_name):
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=user_name)
    post_list = Post.objects.filter(
        author=user, category__isnull=False
    ).select_related('location', 'category', 'author').annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    paginator = Paginator(post_list, PAGINATOR_VALUE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, template, context)


@login_required
def edit_profile(request, user_name):
    user = get_object_or_404(User, username=user_name)
    form = UserForm(request.POST or None, instance=user)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse_lazy('blog:profile',
                                     args=[self.request.user.username]))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if post.author != request.user:
            return redirect('blog:post_detail', id=self.kwargs.get('pk'))
        self.is_editing_post = True
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_editing_post'] = self.is_editing_post
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs.get('pk')}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if post.author != request.user:
            return redirect('blog:post_detail', id=self.kwargs.get('pk'))
        self.is_deleting_post = True
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_deleting_post'] = self.is_deleting_post
        context['form'] = {'instance': self.object}
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        comment = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.post = comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs.get('pk')}
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        if comment.author != request.user:
            return redirect('blog:post_detail', comment.post_id)
        self.is_editing_comment = True
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_editing_comment'] = self.is_editing_comment
        return context

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs.get('post_id')}
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        if comment.author != request.user:
            return redirect('blog:post_detail', id=self.kwargs.get('post_id'))

        self.is_deleting_comment = True
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_deleting_comment'] = self.is_deleting_comment
        return context
