from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login


def post_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'back/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    likes = Like.objects.filter(post=post)
    return render(request, 'back/post_detail.html', {'post': post, 'comments': comments, 'likes': likes})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'back/post_create.html', {'form': form})



def post_list(request):
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'back/post_list.html', {'posts': posts})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'back/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegistrationForm()
    return render(request, "back/register.html", {"form": form})

@login_required
def home(request):
    return render(request, 'back/post_list.html')
