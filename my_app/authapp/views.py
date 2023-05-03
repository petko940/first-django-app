import hashlib

from django.contrib.auth import logout

from django.shortcuts import render, redirect
from authapp.forms import RegisterForm, LoginForm
from authapp.models import Register

from bs4 import BeautifulSoup
import requests


# Create your views here.
def home(request):
    try:
        user = Register.objects.get(id=request.session.get('user_id'))
        is_logged = check_if_someone_logged(request)
        context = {'is_logged': is_logged,
                   'user': user}
        return render(request, 'base.html', context)
    except:
        return render(request, 'base.html')


def check_if_someone_logged(request):
    user_id = request.session.get('user_id')
    if user_id:
        return True


def register_view(request):
    if check_if_someone_logged(request):
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            hashed_password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
            hashed_password2 = hashlib.sha256(password1.encode('utf-8')).hexdigest()

            if password1 == password2:
                user = Register.objects.create(username=username,
                                               email=email,
                                               password1=hashed_password,
                                               password2=hashed_password2)
                user.save()
                request.session['user_id'] = user.id

                return redirect('home')

    else:
        form = RegisterForm()

    placeholders = {'username': 'Username',
                    'email': 'Email',
                    'password1': 'Password',
                    'password2': 'Confirm Password', }

    for field in form.fields:
        form.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if check_if_someone_logged(request):
        return redirect('home')

    placeholders = {'username': 'Username', 'password': 'Password'}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = Register.objects.get(username=username)
            except Register.DoesNotExist:
                error = 'Incorrect username or password'
                for field in form.fields:
                    form.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
                return render(request, 'login.html', {'error': error, 'form': form})
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            if hashed_password == user.password1:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                error = 'Incorrect username or password'
                for field in form.fields:
                    form.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
                return render(request, 'login.html', {'error': error, 'form': form})

    else:
        form = LoginForm()

    for field in form.fields:
        form.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def profile(request):
    user = Register.objects.get(id=request.session.get('user_id'))
    is_logged = check_if_someone_logged(request)
    context = {'is_logged': is_logged,
               'user': user}

    return render(request, 'profile.html', context)

# def profile_edit(request):
#     is_logged = check_if_someone_logged(request)
#
#     # Check if the user is logged in and the user_id session variable exists
#     if is_logged and 'user_id' in request.session:
#         user_id = request.session['user_id']
#
#         try:
#             user = Register.objects.get(id=user_id)
#         except Register.DoesNotExist:
#             # Redirect to an error page or display an error message
#             return HttpResponse("User does not exist")
#
#         if request.method == 'POST':
#             # Save a copy of the existing user data
#             old_username = user.username
#             old_email = user.email
#
#             # Delete the existing user data from the database
#             user.delete()
#
#             # Save the new user data from the form
#             form = RegisterForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('profile')
#             else:
#                 print(form.errors)
#                 # Restore the old user data if the form is not valid
#                 Register.objects.create(username=old_username, email=old_email)
#         else:
#             # Create a new instance of the form with the existing user data
#             form = RegisterForm(instance=user)
#
#         context = {
#             'is_logged': is_logged,
#             'user': user,
#             'form': form
#         }
#         return render(request, 'profile_edit.html', context)
#     else:
#         # Redirect to the login page if the user is not logged in
#         return redirect('login')
