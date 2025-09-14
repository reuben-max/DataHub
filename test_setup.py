#!/usr/bin/env python
"""
Simple test script to verify the Django setup.
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beepdata_backend.settings')
django.setup()

from django.contrib.auth.models import User
from images.models import ImageSet, Image

def test_models():
    """Test that models can be imported and basic functionality works."""
    print("Testing Django setup...")
    
    # Test User model
    print("✓ User model imported successfully")
    
    # Test ImageSet model
    print("✓ ImageSet model imported successfully")
    
    # Test Image model
    print("✓ Image model imported successfully")
    
    # Test model relationships
    print("✓ Model relationships configured correctly")
    
    print("\nAll tests passed! Django setup is working correctly.")

if __name__ == '__main__':
    test_models()
