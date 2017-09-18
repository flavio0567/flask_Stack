from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
# from django.contrib import messages
# from time import gmtime, strftime
# from django.utils.crypto import get_random_string


def index(request):
    return HttpResponse("placeholder to later display all the list of blogs")
    # return render(request, blogs/index.html, {"blogs": Blog.objects.all() })

def new(request):
    return HttpResponse("placeholder to later display a new form tocreate a new blog")
    # return render(request, 'blogs/new.html')

def create(request):
    return redirect('/blogs') 

def show(request, blog_id):
    print blog_id
    return HttpResponse("placeholder to later display blog {}".format(blog_id))
    # return render(request, 'blogs/show.html', { "blog": Blog.objects.get(id = id)})

def edit(request, blog_id):
    return HttpResponse("placeholder to later edit a blog {}".format(blog_id))
    # return render(request, 'blogs/edit.html', { "blog": Blog.objects.get(id = id)})

def destroy(request, blog_id):
    return redirect('/blogs') 

