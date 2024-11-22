from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm, FolderCreateForm
from .models import Photo, PhotoFolder


@login_required
def gallery(request):
    try:
        folders = PhotoFolder.objects.filter(user=request.user)
        if 'folder' in request.GET:
            folder_id = request.GET.get('folder')
            folder = get_object_or_404(PhotoFolder, pk=folder_id, user=request.user) 
            photos = folder.photos.all() 
        else:
            photos = Photo.objects.filter(folder__user=request.user) 

        return render(request, 'gallery.html', {'folders': folders, 'photos': photos})
    except Exception as e:
        print(f"Error in gallery view: {e}")
        return render(request, 'gallery.html', {'folders': [], 'photos': []}) 



@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, user=request.user) 
        if form.is_valid():
            photo = form.save(commit=False)
            photo.folder = form.cleaned_data['folder']
            photo.save()
            return redirect('gallery')
    else:
        form = PhotoUploadForm(initial={'folder': request.GET.get('folder')}, user=request.user) 
    return render(request, 'upload_photo.html', {'form': form})


def upload_photo1(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user 
            photo.save()
            return redirect('gallery') 
    return render(request, 'upload_photo.html', context={'form': form})


@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderCreateForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect('gallery')
    else:
        form = FolderCreateForm()
    return render(request, 'create_folder.html', {'form': form})






def folder_detail(request, pk):
    try:
        folder = PhotoFolder.objects.get(pk=pk)
        if request.method == 'POST':
            form = PhotoUploadForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.folder = folder
                photo.save()
                return redirect('folder_detail', pk=pk) 
        else:
            form = PhotoUploadForm(initial={'folder': request.GET.get('folder')}, user=request.user)

        photos = folder.photos.all()
        return render(request, 'folder_detail.html', {'folder': folder, 'photos': photos, 'form': form})
    except ObjectDoesNotExist:
        return HttpResponse("Папка не найдена", status=404)



def photo_delete(request, pk):
    if request.method == 'POST':
        try:
            photo = Photo.objects.get(pk=pk)
            photo.delete()
            return redirect('folder_detail', pk=photo.folder.pk)
        except ObjectDoesNotExist:
            return HttpResponse("Фотография не найдена", status=404)
    return HttpResponse("Ошибка метода запроса")

def folder_delete(request, pk):
    if request.method == 'POST':
        try:
            folder = PhotoFolder.objects.get(pk=pk)
            folder.photos.all().delete()
            folder.delete()
            return redirect('gallery')
        except ObjectDoesNotExist:
            return HttpResponse("Папка не найдена", status=404)
    return HttpResponse("Ошибка метода запроса")





from .forms import PhotoEditForm


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = PhotoEditForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('folder_detail', pk=photo.folder.pk)
    else:
        form = PhotoEditForm(instance=photo)
    return render(request, 'photo_detail.html', {'photo': photo, 'form': form})









