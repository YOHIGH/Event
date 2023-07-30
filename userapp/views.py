from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect('success_url')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def success_page(request):
    return render(request, 'auth/success.html')


@login_required
def profile(request):
    return render(request, 'content/profile.html')
