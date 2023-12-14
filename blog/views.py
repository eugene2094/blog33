from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import time

from django.utils import timezone

from .forms import PostForm, CommentForm, UserProfileForm
from .models import Post, Category, Comment


def get_categories():
    all = Category.objects.all()
    count = all.count()
    return {'cat1': all[:count / 2 + count % 2], 'cat2': all[count / 2 + count % 2:]}


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by("-published_date")
    # postid = Post.objects.get(pk=1)
    # posts = Post.objects.filter(title__contains="js")
    # posts = Post.objects.filter(published_date__year=2022)
    # posts = Post.objects.filter(category__name__iexact='Python')
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)


def post(request, id=None):
    post = get_object_or_404(Post, title=id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return render(request, "blog/post.html",
                          context={'post': post, 'comment_form': comment_form, 'comments': comments})

    context = {"post": post, "comments": comments, 'comment_form': comment_form}
    context.update(get_categories())
    return render(request, "blog/post.html", context=context)


def about(request):
    return render(request, "blog/about.html")


def contacts(request):
    return render(request, "blog/contacts.html")


def services(request):
    return render(request, "blog/services.html")


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.user = request.user
            post.save()
            return index(request)
    form = PostForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/create.html', context=context)


def register(request):
    # if request.method == 'POST':
    #     form = UserProfileForm(request.POST)
    #     if form.is_valid():
    #         new_user = form.save(commit=False)
    #         User.objects.create_user()
    #         post.save()
    #         return index(request)
    form = UserProfileForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, "blog/registration_user.html", context=context)
