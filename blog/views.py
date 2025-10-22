from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from blog.models import Post
# Create your views here.


def post_list(request, year=None, month=None, code=None):
    if month is not None:
        return HttpResponse(f"post list archive for {year} and  {month}")

    if year is not None:
        return HttpResponse(f"post list archive for {year}")

    if code is not None:
        return HttpResponse(f"gift code is {code}")

    return HttpResponse("<h1>H1 tag</h1><br><h2>H2 tag</h2>")



class BlogPostLisView(ListView):
    model = Post



def categories_list(request, post_title):

    return HttpResponse(f"categories list page {post_title}")


def post_detail(request, post_title):
    return HttpResponse(f"Post detail {post_title}") 


class BlogPostDetailView(DetailView):
    model = Post



# def about(request):
#     return render(request, 'about.html')