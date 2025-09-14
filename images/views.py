from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import ImageSet, Image
from .serializers import (
    ImageSetSerializer, 
    ImageUploadSerializer, 
    UserSerializer,
    ImageSerializer
)


class ImageSetListCreateView(generics.ListCreateAPIView):
    """
    List all ImageSets for the authenticated user or create a new one.
    """
    serializer_class = ImageSetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ImageSet.objects.filter(user=self.request.user)


class ImageSetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an ImageSet.
    """
    serializer_class = ImageSetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ImageSet.objects.filter(user=self.request.user)


class ImageUploadView(generics.CreateAPIView):
    """
    Upload an image to a specific ImageSet.
    """
    serializer_class = ImageUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        image_set_id = kwargs.get('image_set_id')
        image_set = get_object_or_404(ImageSet, id=image_set_id, user=request.user)
        
        serializer = self.get_serializer(data=request.data)
        serializer.context['image_set_id'] = image_set_id
        
        if serializer.is_valid():
            # Create the image
            image = Image.objects.create(
                image_set=image_set,
                image_type=serializer.validated_data['image_type'],
                image_file=serializer.validated_data['image_file']
            )
            
            # Return the created image
            image_serializer = ImageSerializer(image, context={'request': request})
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDeleteView(generics.DestroyAPIView):
    """
    Delete an image from an ImageSet.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Image.objects.filter(image_set__user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Login endpoint to authenticate users and return a token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': user_serializer.data
        })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint to delete the user's token.
    """
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response(
            {'error': 'Token not found'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """
    Register a new user.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    
    token = Token.objects.create(user=user)
    user_serializer = UserSerializer(user)
    
    return Response({
        'token': token.key,
        'user': user_serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile_view(request):
    """
    Get the current user's profile.
    """
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data)
