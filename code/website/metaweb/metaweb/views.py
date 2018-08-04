from django.shortcuts import HttpResponse, render, redirect


# Create your views here.

def index(request):
    return redirect('/home')