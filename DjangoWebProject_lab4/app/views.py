from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Blog
from .models import Comment 
from .forms import CommentForm 
from .forms import BlogForm

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/index.html",
        {
            "title": "Главная",
            "year": datetime.now().year,
        },
    )

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/videopost.html",
        {
            "title": "Видео",
            "year": datetime.now().year,
        },
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():  # валидация полей формы
            reg_f = regform.save(commit=False)  # не сохраняем автоматически
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            reg_f.save()  # сохраняем изменения
            return redirect('home')
    else:
        # создание объекта формы для ввода данных нового пользователя
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    
    # Запрос на выбор всех статей блога из модели
    posts = Blog.objects.all() 
    
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,  # Передача списка статей в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    
    post_1 = Blog.objects.get(id=parametr) 
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":  
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user 
            comment_f.date = datetime.now() 
            comment_f.post = post_1 
            comment_f.save() 
            
            return redirect('blogpost', parametr=parametr) 
    else:
       
        form = CommentForm() 

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":                       # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()                              # сохраняем изменения после добавления полей
            
            return redirect('blog')                    # переадресация на страницу Блог после создания статьи блога
    else:
        blogform = BlogForm()                          # создание объекта формы для ввода данных
        
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,                      # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )

