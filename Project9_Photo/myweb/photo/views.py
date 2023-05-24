from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo
from .forms import PhotoForm

# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'photo/photo_list.html', context)

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    context = {'photo': photo}
    return render(request, 'photo/photo_detail.html', context)

def photo_post(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    context = {'form': form}
    return render(request, 'photo/photo_post.html', context)

def photo_edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, instance=photo)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            return redirect('photo_detail', pk=pk)
    else:
        form = PhotoForm(instance=photo)
    context = {'form': form}
    return render(request, 'photo/photo_post.html', context)