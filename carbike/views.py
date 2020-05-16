from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("hello")

def predict(request):
    return HttpResponse("hellwwwo")