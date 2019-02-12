import datetime

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import pic
from PIL import Image
# Create your views here.


def index(request):
    return render(request, 'index2.html')


def upload(request):
    x = datetime.datetime.now()
    uploadedname = str(request.FILES['fileToUpload']).split('.')
    fname = '%s.%s.%s.%s.%s.%s.%s' % (x.year, x.month, x.day, x.hour, x.minute, x.second, uploadedname[-1])
    name = default_storage.save(fname, request.FILES['fileToUpload'])
    m = pic(name = name)
    m.save()
    redirect_path = '/up/edit/%s/' % m.pk
    return redirect(redirect_path)


def edit(request, key):
    im = pic.objects.get(pk=key)
    if im.edited :
        return render(request, 'cannotedit.html')
    else:
        context = {
            'pic_url':'media/%s' % im.name,
        }
        return render(request, 'edit.html', context)


def bl (request, key):
    im = pic.objects.get(pk=key)
    if im.edited:
        return render(request, 'cannotedit.html')
    else:
        im2edit = Image.open('media/%s' % im.name).convert("L").save('media/%s' % im.name)
        redirect_path = '/up/edit/%s/' % key
        return redirect(redirect_path)


def rotatation(request, key):
    im = pic.objects.get(pk=key)
    if im.edited:
        return render(request, 'cannotedit.html')
    else:
        im2edit = Image.open('media/%s' % im.name)
        im2edit = im2edit.rotate()
    return