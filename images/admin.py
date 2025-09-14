from django.contrib import admin
from .models import ImageSet, Image


@admin.register(ImageSet)
class ImageSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'is_complete', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def is_complete(self, obj):
        return obj.images.count() == 3
    is_complete.boolean = True
    is_complete.short_description = 'Complete'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_set', 'image_type', 'uploaded_at']
    list_filter = ['image_type', 'uploaded_at']
    search_fields = ['image_set__title', 'image_set__user__username']
    readonly_fields = ['uploaded_at']
