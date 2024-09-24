from django.shortcuts import render


def login(request):
    return render(request, 'accounts/login-page.html')


def register(request):
    return render(request, 'accounts/register-page.html')


def profile_delete(request, pk: int):
    return render(request, 'accounts/profile-delete-page.html')


def profile_details(request, pk: int):
    return render(request, 'accounts/profile-details-page.html')


def profile_edit(request, pk: int):
    return render(request, 'accounts/profile-edit-page.html')
