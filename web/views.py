import os

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from .models import Photo, Gallery


def index(request):
    gallery_list = Gallery.objects.all()

    context = {
        'gallery_list': gallery_list
    }

    return render(request, 'web/index.html', context=context)


def gallery(request):
    galleries = Gallery.objects.all()
    gallery_list = []
    if len(galleries):
        for gallery in galleries:
            item = {
                'gallery': gallery,
                'photos': gallery.photo_set.all()
            }
            gallery_list.append(item)

    context = {
        'gallery_list': gallery_list
    }

    return render(request, 'web/gallery.html', context=context)


def update_gallery(request):
    if request.method == "POST":
        gallery_id = int(request.POST.get('photo_id'))
        gallery = Gallery.objects.get(id=gallery_id)
        origin_gallery_photo = gallery.gallery_image.path
        try:
            os.remove(origin_gallery_photo)
        except Exception as e:
            pass
        gallery.gallery_image = request.FILES.get('image')
        gallery.save()
        return HttpResponse({'success': 'success'}, status=200)


def gallery_detail(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)
    photos = gallery.photo_set.all()

    context = {
        'photos': photos
    }

    return render(request, 'web/gallery_content.html', context=context)


def change_photo(request):
    if request.method == 'POST':
        photo_id = int(request.POST.get('photo_id'))
        photo = Photo.objects.get(id=photo_id)
        origin_photo = photo.photo.path
        try:
            os.remove(origin_photo)
        except Exception as e:
            pass
        photo.photo = request.FILES.get('image')
        photo.save()
        return HttpResponse({'success': 'success'}, status=200)


def delete_photo(request):
    if request.method == 'POST':
        photo_id = int(request.POST.get('photo_id'))
        photo = Photo.objects.get(id=photo_id)
        try:
            os.remove(photo.photo.path)
        except Exception as e:
            pass
        photo.delete()
        return HttpResponse({'success': 'success'}, status=200)


def add_new_photo(request):
    if request.method == 'POST':
        gallery_id = int(request.POST.get('gallery_id'))
        gallery = Gallery.objects.filter(id=gallery_id).first()
        photo = Photo.objects.create(
            name=request.POST.get('name'),
            photo=request.FILES.get('image'),
            gallery=gallery
        )

        return HttpResponse({'success': 'success'}, status=200)
