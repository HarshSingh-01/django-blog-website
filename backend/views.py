from django.shortcuts import render
from django.db.models import Q
from .models import Author, Category, Post
import datetime

# Create your views here.

def homepage(request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'object_list': featured,
        'latest':latest,
        'categories': categories,
    }

    return render(request, 'homepage.html', context=context)

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def post(request, slug):
    post = Post.objects.get(slug=slug)
    context = {
        'post': post
    }

    return render(request, 'post.html', context)

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        try:
            queryset = queryset.filter( Q(title_icontains=query) | Q(overview_icontains=query) ).distinct()
        except:
            pass

    context = {
            'object_list': queryset
        }
    
    return render(request, 'search_bar.html', context)


def about(request):
    dob_string = "2000-02-01"
    dob = datetime.datetime.strptime(dob_string, "%Y-%m-%d")
    now =  datetime.datetime.now()
    difference = now - dob
    age = difference.days / 365.2425
    age = int(age)
    context = {
        'age':age
    }
    return render(request, 'about_page.html', context)


def postlist(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(categories__in=[category])
    context ={
        'posts':posts,
    }

    return render(request, 'post_list.html', context)


def allposts(request):
    posts = Post.objects.order_by('-timestamp')
    context = {
        'posts': posts,
    }

    return render(request, 'all_posts.html', context)


