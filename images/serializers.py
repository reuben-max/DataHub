from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ImageSet, Image


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for individual images.
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = ['id', 'image_type', 'image_file', 'image_url', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def get_image_url(self, obj):
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        return None


class ImageSetSerializer(serializers.ModelSerializer):
    """
    Serializer for ImageSet with nested images.
    """
    images = ImageSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    is_complete = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageSet
        fields = [
            'id', 'user', 'title', 'description', 'images', 
            'is_complete', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_is_complete(self, obj):
        """
        Check if the ImageSet has all three required images.
        """
        return obj.images.count() == 3
    
    def create(self, validated_data):
        """
        Create ImageSet with the current user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ImageUploadSerializer(serializers.Serializer):
    """
    Serializer for uploading individual images to an ImageSet.
    """
    image_file = serializers.ImageField()
    image_type = serializers.ChoiceField(choices=Image.IMAGE_TYPES)
    
    def validate_image_type(self, value):
        """
        Validate that the image type is not already used in the ImageSet.
        """
        image_set_id = self.context.get('image_set_id')
        if image_set_id:
            if Image.objects.filter(image_set_id=image_set_id, image_type=value).exists():
                raise serializers.ValidationError(
                    f"Image of type '{value}' already exists for this ImageSet."
                )
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']
