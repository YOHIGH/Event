from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .utils import generate_jwt_token, validate_jwt_token
from django.http import JsonResponse
import json


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token = generate_jwt_token(user.id)
            request.session['jwt_token'] = token
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return render(request, 'auth/login.html')


def success_page(request):
    return render(request, 'auth/success.html')


@login_required
def profile(request):
<<<<<<< Updated upstream
    jwt_token = request.session.get('jwt_token', None)
    user_id = validate_jwt_token(jwt_token)
=======
    token = request.GET['token']
    user_id = validate_jwt_token(token)
>>>>>>> Stashed changes

    if user_id is None:
        return JsonResponse({'error': 'Invalid or expired token'}, status=401)

    return render(request, 'content/profile.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('user/profile')
    return redirect('user/login')