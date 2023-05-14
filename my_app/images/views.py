import base64

from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from authapp.models import Register
from authapp.views import check_if_someone_logged
from images.forms import ImageForm
from images.models import Image


# Create your views here.
def image_upload(request):
    try:
        user = Register.objects.get(id=request.session.get('user_id'))
        is_logged = check_if_someone_logged(request)
    except Register.DoesNotExist:  # NOQA
        return redirect('home')

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = request.FILES.get('image_data', None)  # Use get() method with default value
            if image_data:
                try:
                    image_data = image_data.read()
                    image_model = Image.objects.create(
                        image_data=image_data,
                        image_name=request.POST['image_name'],
                        user=user
                    )
                    image_data_base64 = base64.b64encode(image_model.image_data).decode('utf-8')

                    context = {
                        'form': form,
                        'image_data_base64': image_data_base64,
                        'success_message': 'Image uploaded successfully!'
                    }
                    return render(request, 'image_upload.html', context)
                except Register.DoesNotExist:
                    context = {
                        'form': form,
                        'is_logged': is_logged,
                        'user': user,
                        'error': 'Choose file'
                    }
                    return render(request, 'image_upload.html', context)
            else:
                return HttpResponseBadRequest('No file was uploaded.')
    else:
        form = ImageForm()

    context = {
        'form': form,
        'is_logged': is_logged,
        'user': user
    }
    return render(request, 'image_upload.html', context)


def images_show(request):
    try:
        user = Register.objects.get(id=request.session.get('user_id'))
        is_logged = check_if_someone_logged(request)
    except:  # NOQA
        return redirect('home')

    images = Image.objects.filter(user=user)

    context = {'images': images,
               'is_logged': is_logged,
               'user': user}
    return render(request, 'images_show.html', context)


def delete_image(request, image_id):
    try:
        image = get_object_or_404(Image, id=image_id)
        image.delete()
    except Image.DoesNotExist:
        return HttpResponse("Image not found.")

    return redirect('images_show')