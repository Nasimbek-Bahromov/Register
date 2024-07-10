from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

def blogs(request):
    posts = models.Blog.objects.all()
    for post in posts:
        post.img = models.BlogImg.objects.filter(blog__id = post.id).last()
    context = {
        'posts':posts
    }
    print(dir(posts))
    return render(request, 'blogs.html', context)


def blog_detail(request, id):
    blog = models.Blog.objects.get(id=id)
    user = blog.author
    # comment_count = models.Comment.objects.filter(blog=blog).count()
    comments = models.Comment.objects.filter(blog=blog)
    context = {
        'blog':blog,
        # 'comment_count':comment_count,
        'comment_count':comments.count(),
        'comments':comments,
        'user':user
    }
    return render(request, 'blog-detail.html', context)


def comment_create(request):
    message = request.POST['message']
    blog_id = request.POST['blog_id']
    models.Comment.objects.create(
        author=request.user,
        body=message,
        blog_id=blog_id
    )
    return redirect('blog_detail', blog_id)


def register_user(request):
    if request.method == 'POST':
        User.objects.create_user(
            username = request.POST['username'],
            password = request.POST['password']
        )
    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('index')