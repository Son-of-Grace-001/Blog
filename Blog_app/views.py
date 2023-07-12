from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def home(request):
    posts = Blog.objects.all()
    context ={"posts": posts}
    return render(request, 'Blog/home.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not username or not email or not password:
            print("Incomplete details")
        else:
            new_user = User(username=username, email=email, password=password)
            new_user.save()
            return redirect(reverse("home"))
    return render(request, 'Blog/signup.html')

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      if username is None or password is None:
        messages.info(request, 'username or password not found')
        return redirect('/login')
      user = auth.authenticate (username=username, password=password)
      if user is None:
          messages.info(request, 'Invalid login credentials')
          return redirect('/login')
      auth.login(request, user)
      return redirect(reverse("home"))
    return render(request, 'Blog/login.html')

def logout(request):
    auth.logout(request)
    return redirect(reverse("home"))


@login_required
def create(request):
    if request.method == 'POST':
        author = request.user
        title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('content')
        if title is None or category is None or content is None:
            return redirect('/create')
        else:
            create_blog = Blog.objects.create(title=title, category=category, content=content, author=author)
            create_blog.save()
            return redirect(reverse("home"))
    return render (request, 'Blog/create.html')

def read(request,id):
    try:
        post = Blog.objects.get(id=id)
        context = {"post":post}
    except:
        context = {"post": None}
    return render(request, "Blog/read.html", context)

@login_required
def delete (request, id):
    post = Blog.objects.get(id=id)
    if post.author == request.user:
        post.delete()
    return redirect(reverse('home'))


@login_required
def edit (request, id):
    post = Blog.objects.get(id=id)
    context = {"post":post}
    if post.author != request.user:
       messages.info(request,"you are not authorized")
       return redirect (reverse("home"))
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        content = request.POST.get("content")
        img = request.FILES.get("img")
        if img:
            post.image = img
        post.title = title
        post.category = category
        post. content = content
        post.save()

        messages.info(request, "post edited successfully")
        return redirect (reverse ("home"))
    return render (request, "Blog/edit.html", context)

        


