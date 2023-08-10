from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .utils import generate_jwt_token, validate_jwt_token
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger('root')


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
    logger.info(f"User_logged_in: {request}")
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
    jwt_token = request.session.get('jwt_token', None)
    user_id = validate_jwt_token(jwt_token)

    if user_id is None:
        return JsonResponse({'error': 'Invalid or expired token'}, status=401)

    return render(request, 'content/profile.html')


def home(request):
    if request.user.is_authenticated:
        return redirect('user/profile')
    return redirect('user/login')


def profile_details(request):
    user = request.user

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)

            attributes_to_update = ['email', 'phone_number', 'address', 'date_of_birth', 'gender', 'country', 'city', 'state']

            for attribute in attributes_to_update:
                value = data.get(attribute)
                if value is not None:
                    setattr(user, attribute, value)

            if any(data.get(attribute) is not None for attribute in attributes_to_update):
                user.save()

            return JsonResponse({'message': 'Profile details updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    return render(request, 'content/profile.html', {'user': user})
