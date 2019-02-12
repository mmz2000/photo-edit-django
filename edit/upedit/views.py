import datetime

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import pic
from PIL import Image
# Create your views here.

supported_formats=[
    'BPM',
    'EPS',
    'GIF',
    'ICNS',
    'ICO',
    'IM',
    'JPEG',
    'JPG',
    'MSP',
    'PNG',
    'PCX',
    'PPM',
    'SGI',
]
def index(request):
    return render(request, 'index2.html')


def upload(request):
    x = datetime.datetime.now()
    uploadedname = str(request.FILES['fileToUpload']).split('.')
    fname = '%s.%s.%s.%s.%s.%s.%s' % (x.year, x.month, x.day, x.hour, x.minute, x.second, uploadedname[-1])
    if not uploadedname[-1].upper() in supported_formats:
        return render(request, 'notsupported.html')
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
            'rotate_url':'rt/',
            'resize_url':'rs/',
            'crop_url':'cr/'
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
        try:
            im2edit = im2edit.rotate(
                int(request.POST['deg'])).save('media/%s' % im.name)
        except:
            return render(request,'wronginput.html')
        redirect_path = '/up/edit/%s/' % key
        return redirect(redirect_path)


def croper (request, key):
    im = pic.objects.get(pk=key)
    if im.edited:
        return render(request, 'cannotedit.html')
    else:
        im2edit = Image.open('media/%s' % im.name)
        try:
            x1 = int(request.POST['x1'])
            y1 = int(request.POST['y1'])
            x2 = int(request.POST['x2'])
            y2 = int(request.POST['y2'])
        except:
            return render(request, 'wronginput.html')
        if (x1>=x2)or(y1>=y2):
            return render(request, 'wronginput2.html')
        im2edit = im2edit.crop((x1, y1, x2, y2))
        im2edit.save('media/%s' % im.name)
        redirect_path = '/up/edit/%s/' % key
        return redirect(redirect_path)


def resizer (request,key):
    im = pic.objects.get(pk=key)
    if im.edited:
        return render(request, 'cannotedit.html')
    else:
        im2edit = Image.open('media/%s' % im.name)
        try:    
            x = int(request.POST['w_size'])
            y = int(request.POST['h_size'])
        except:
            return render(request, 'wronginput.html')
        im2edit = im2edit.resize((x,y))
        im2edit.save('media/%s' % im.name)
        redirect_path = '/up/edit/%s/' % key
        return redirect(redirect_path)


def share (request, key):
    im = pic.objects.get(pk=key)
    im.edited=True
    im.save()
    return redirect('/')


def feed (request):
    pic_names=[]
    for i in pic.objects.all():
        if i.edited :
            pic_names.append(i.name)
    pic_names.sort()
    pic_names.reverse()
    context={
        'list':pic_names
    }
    return render(request, 'feed.html', context)

