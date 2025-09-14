from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import ImageSet, Image
import json


def login_page(request):
    """Render the login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'images/login.html')


@csrf_exempt
@require_http_methods(["POST"])
def web_login(request):
    """Handle web-based login"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/dashboard/'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def web_register(request):
    """Handle web-based registration"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Auto-login after registration
        login(request, user)
        return JsonResponse({'success': True, 'redirect': '/dashboard/'})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def dashboard(request):
    """Render the dashboard page"""
    image_sets = ImageSet.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'image_sets': image_sets,
        'user': request.user
    }
    return render(request, 'images/dashboard.html', context)


@login_required
def logout_view(request):
    """Handle logout"""
    logout(request)
    return redirect('login')
