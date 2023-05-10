from django.urls import path

from images import views

urlpatterns = [
    path('images/upload', views.image_upload, name='image_upload'),
    path('images', views.images_show, name='images_show'),
    path('image/delete/<image_id>/', views.delete_image, name='delete_image'),
]
