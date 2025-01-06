from django.shortcuts import render

def home(request):
    """
    Renders the home page.
    """
    return render(request, 'main/home.html')



# views.py
from django.shortcuts import render
from .models import GalleryImage

def home(request):
    gallery_images = GalleryImage.objects.all()
    return render(request, 'main/home.html', {'gallery_images': gallery_images})
