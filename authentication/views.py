from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from authentication.models import LoginForm
from smart_labeler.constants import MAIN_PAGE_TEMPLATE


# Create your views here.

def starting_page(request):
    if request.user:
        return redirect('upload-page')
    return render(request, MAIN_PAGE_TEMPLATE, {"is_auth": False})


def post_login(request):
    if request.method != 'POST':
        return render(request, MAIN_PAGE_TEMPLATE, {"is_auth": False})
    form = LoginForm(request.POST)
    print(form.is_valid())
    print(form.errors)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        authenticated_user = authenticate(request, username=username, password=password)
        if not authenticated_user:
            return redirect('main-page')
        login(request, authenticated_user)
        return redirect('upload-page')
    return render(request, MAIN_PAGE_TEMPLATE, {'form': form, "is_auth": False})


@login_required
def perform_logout(request):
    logout(request)
    return redirect('main-page')
