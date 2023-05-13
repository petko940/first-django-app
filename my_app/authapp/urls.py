from django.urls import path
from authapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register_view, name='register_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('profile', views.profile, name='profile'),
    path('profile/delete', views.profile_delete, name='profile_delete'),
    # path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/<image_id>/', views.change_profile_picture, name='change_profile_picture'),
]
