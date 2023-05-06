import hashlib
from datetime import datetime

from django.contrib.auth import logout
from django.http import HttpResponse

from django.shortcuts import render, redirect
from authapp.forms import RegisterForm, LoginForm
from authapp.models import Register


from weather.models import City


# Create your views here.
def page_not_found(request, exception):
    return HttpResponse("Page not found", status=404)


def home(request):
    try:
        user = Register.objects.get(id=request.session.get('user_id'))
        is_logged = check_if_someone_logged(request)
        context = {'is_logged': is_logged,
                   'user': user}
        return render(request, 'base.html', context)
    except:  # NOQA
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
    if not check_if_someone_logged(request):
        return redirect('home')

    user = Register.objects.get(id=request.session.get('user_id'))
    is_logged = check_if_someone_logged(request)
    context = {'is_logged': is_logged,
               'user': user}

    return render(request, 'profile.html', context)


def profile_delete(request):
    is_logged = check_if_someone_logged(request)
    user = Register.objects.get(id=request.session.get('user_id'))
    cities = City.objects.filter(user=user)

    if request.method == 'POST':
        user.delete()
        cities.delete()
        request.session.flush()
        return redirect('home')

    context = {'user': user,
               'is_logged': is_logged}
    return render(request, 'profile_delete.html', context)


