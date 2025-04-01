from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django_ratelimit.decorators import ratelimit

from minimal_user.forms import LoginForm, RegistrationForm
from django.shortcuts import redirect, render

from minimal_user.safe_sql import find_user_by_username


@ratelimit(key='ip', rate='5/m', block=True)
def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration. Limits to 5 attempts per minute by IP.
    :param request: HttpRequest
    :return: Rendered registration form or redirect to login.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'minimal_user/register.html',
                  {'form': form})


@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user login. Limits to 5 attempts per minute by IP.
    :param request: HttpRequest
    :return: Login page or redirect to homepage.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request=request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.error(request, 'Invalid username or password')

    else:
        form = LoginForm()
    return render(request, 'minimal_user/login.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logs the user out and redirects to login page.
    :param request: HttpRequest
    :return: Redirect to login view.
    """
    logout(request)
    return redirect('login')


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the homepage. Shows user-specific content if logged in.
    :param request: HttpRequest
    :return: Rendered home page.
    """
    return render(request, 'minimal_user/home.html', {'user': request.user})


@login_required
def user_lookup_view(request: HttpRequest) -> HttpResponse:
    """
    A protected view that allows authenticated users to look up other users
    by username via a GET parameter (?username=...).
    :param request: HttpRequest
    :return: Rendered result page with user info (or none if not found).
    """
    user_data = None
    username = request.GET.get('username')
    if username:
        user_data = find_user_by_username(username)
    return render(request, 'minimal_user/lookup.html', {'user_data': user_data})
