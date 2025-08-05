from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def post_list(request, year=None, month=None, code=None):
    if month is not None:
        return HttpResponse(f"post list archive for {year} and  {month}")

    if year is not None:
        return HttpResponse(f"post list archive for {year}")

    if code is not None:
        return HttpResponse(f"gift code is {code}")

    return HttpResponse("post list page")


def categories_list(request, post_title):

    return HttpResponse(f"categories list page {post_title}")


def post_detail(request, post_title):
    return HttpResponse(f"Post detail {post_title}")
