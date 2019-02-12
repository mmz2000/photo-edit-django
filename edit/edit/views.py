from django.shortcuts import render
from django.template.loader import get_template


def index(request):
    return render(request, 'index1.html')
