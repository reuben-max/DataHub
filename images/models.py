from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class ImageSet(models.Model):
    """
    Model to bundle three images together as a set.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_sets')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"ImageSet {self.id} by {self.user.username}"


class Image(models.Model):
    """
    Model for individual images within an ImageSet.
    """
    IMAGE_TYPES = [
        ('input', 'Input'),
        ('dress', 'Dress'),
        ('final', 'Final'),
    ]
    
    image_set = models.ForeignKey(ImageSet, on_delete=models.CASCADE, related_name='images')
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPES)
    image_file = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['image_set', 'image_type']
        ordering = ['image_type']
    
    def __str__(self):
        return f"{self.image_type} for ImageSet {self.image_set.id}"
