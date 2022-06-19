from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.




def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )


def landing(request):
    return render(request, 'single_pages/landing.html')

def todo(request):
    return render(request, 'single_pages/../blog/templates/todolist/todolist.html')
