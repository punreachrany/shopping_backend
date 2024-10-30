# uploads/views.py

from django.shortcuts import render, redirect
from .forms import ImageUploadForm

def upload_image(request):
    if request.method == 'POST':
        print("POST = ", request.POST)
        print("FILE = ", request.FILES)
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Save time")
            return redirect('upload_image')  # Redirect to a success page or same page
    else:
        print("Other time time")
        form = ImageUploadForm()
    print("Render Time")
    return render(request, 'upload_image.html', {'form': form})
