import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import UploadForm, WebMedia


@login_required
def upload_media(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'upload/index.html', {'is_auth': True})


@login_required
def about_page(request):
    if request.method == 'GET':
        return render(request, 'about/index.html', {'is_auth': True})


@login_required
def handle_upload(request):
    form = UploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'upload/index.html', {'is_auth': True, 'form': form})
    media_type = form.cleaned_data.get('media_type')
    media = form.cleaned_data.get('media')
    web_media = WebMedia()
    web_media.user = request.user
    web_media.media_type = media_type
    web_media.filename = media.name
    web_media.media = media.read()
    web_media.save()
    return render(request, 'upload/index.html', {'is_auth': True})


def handle_label_page(request):
    if request.method == "GET":
        media_list = WebMedia.objects.all()
        return render(request, 'label/index.html', {"is_auth": True, "media_list": media_list})


def label_image(request, pk):
    if request.method == "GET":
        print('id', pk)
        web_media = WebMedia.objects.get(id=pk)
        return render(request, 'label/label-detail.html', {"is_auth": True, "id": pk, "media": web_media})


@csrf_exempt
def save_label_data(request, pk):
    print("Saving labelling data")
    web_media = WebMedia.objects.get(id=pk)
    data = request.body.decode('utf-8')
    web_media.labelling_data = data
    web_media.save()
    print('Labelling Data Saved')
    return JsonResponse({"redirectPath": "/home/"})
