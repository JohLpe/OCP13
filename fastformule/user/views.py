from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages


def user_registration(request):
    """Renders user registration page"""

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'registration.html', context={'form': form})


def user_login(request):
    """Renders user loggin page"""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,
                            password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')

        else:
            messages.info(request, "Erreur d'authentification!"
                                   "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html')


def user_logout(request):
    """Renders user logout page"""

    logout(request)
    return redirect('homepage')


def view_account(request):
    """Shows user account"""

    current_user = request.user
    form = PasswordChangeForm(user=current_user, data=request.POST)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        if current_user.check_password(old_password):
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Mot de passe modifié!")
            else:
                messages.error(request,
                               "Nouveaux mot de passe non identiques.")
        else:
            messages.error(request, "Mot de passe erroné.")
    return render(request, 'account.html', {
        'form': form,
    })