#!/usr/bin/env python
"""
Startup script for the Django development server.
"""
import os
import sys
import subprocess

def main():
    """Start the Django development server."""
    print("Starting BeepData Backend Django server...")
    print("Server will be available at: http://localhost:8000")
    print("API endpoints will be available at: http://localhost:8000/api/")
    print("Admin interface will be available at: http://localhost:8000/admin/")
    print("\nPress Ctrl+C to stop the server.\n")
    
    try:
        # Start the Django development server
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        print("Make sure you have installed all dependencies with: pip install -r requirements.txt")

if __name__ == '__main__':
    main()
