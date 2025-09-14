from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from images.models import ImageSet, Image

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    """Render the dashboard for authenticated users"""
    # Fetch image sets for the current user
    image_sets = ImageSet.objects.filter(user=request.user).prefetch_related('images')
    context = {
        'image_sets': image_sets
    }
    return render(request, 'dashboard.html', context)

@login_required
def browse_view(request):
    """Render the browse/gallery view for authenticated users"""
    # Fetch image sets for the current user
    image_sets = ImageSet.objects.filter(user=request.user).prefetch_related('images')
    context = {
        'image_sets': image_sets
    }
    return render(request, 'browse.html', context)

@login_required
def upload_view(request):
    """Render the upload view for authenticated users and handle form submission"""
    if request.method == 'POST':
        try:
            # Get the next image set number
            user_image_sets_count = ImageSet.objects.filter(user=request.user).count()
            next_number = user_image_sets_count + 1
            
            # Create new ImageSet
            image_set = ImageSet.objects.create(
                user=request.user,
                title=f"Image Set {next_number}"
            )
            
            # Create images for each uploaded file
            image_mappings = {
                'input_image': 'input',
                'dress_image': 'dress', 
                'final_image': 'final'
            }
            
            for form_field, image_type in image_mappings.items():
                if form_field in request.FILES:
                    Image.objects.create(
                        image_set=image_set,
                        image_type=image_type,
                        image_file=request.FILES[form_field]
                    )
            
            return JsonResponse({
                'success': True,
                'message': f'Image Set {next_number} created successfully!',
                'image_set_id': image_set.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return render(request, 'upload.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')
