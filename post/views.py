from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def home(request):
    posts = Post.objects.all().order_by("-created_at")[:5]  # Get 5 most recent posts
    return render(request, "insightfulbyte/home.html", {"posts": posts})


def contact(request):
    return render(request, "insightfulbyte/contact.html")


def about(request):
    return render(request, "insightfulbyte/about.html")


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "insightfulbyte/detail-post.html", {"post": post})


def post_display(request):
    posts = Post.objects.all()
    return render(request, "insightfulbyte/post-display.html", {"posts": posts})


@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post.objects.create(title=title, content=content, user=request.user)
        return redirect("detail-post", post_id=post.id)
    return render(request, "insightfulbyte/create-post.html")


@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("detail-post", post_id=post.id)
    return render(request, "insightfulbyte/post_form.html", {"post": post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "insightfulbyte/post_confirm_delete.html", {"post": post})


def all_posts(request):
    posts = Post.objects.all()
    return render(request, "insightfulbyte/all-posts.html", {"posts": posts})


@login_required
def my_posts(request):
    if not hasattr(request, "user") or not request.user.is_authenticated:
        return redirect("login")

    user_obj = request.user
    posts = Post.objects.filter(user=user_obj)
    return render(request, "insightfulbyte/my-posts.html", {"posts": posts})
