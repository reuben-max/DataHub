# BeepData Backend

A Django REST API backend for uploading and managing image sets with authentication.

## Features

- User authentication (login, logout, register)
- Image set management (create, read, update, delete)
- Upload up to 3 images per set
- Token-based authentication
- CORS support for frontend integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your secret key
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user  
- `POST /api/auth/register/` - Register new user
- `GET /api/auth/profile/` - Get user profile

### Image Sets
- `GET /api/imagesets/` - List user's image sets
- `POST /api/imagesets/` - Create new image set
- `GET /api/imagesets/{id}/` - Get image set details
- `PUT /api/imagesets/{id}/` - Update image set
- `DELETE /api/imagesets/{id}/` - Delete image set

### Images
- `POST /api/imagesets/{id}/images/` - Upload image to set
- `DELETE /api/images/{id}/` - Delete image

## Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Create an image set
```bash
curl -X POST http://localhost:8000/api/imagesets/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Image Set", "description": "A set of three images"}'
```

### Upload an image
```bash
curl -X POST http://localhost:8000/api/imagesets/1/images/ \
  -H "Authorization: Token your-token-here" \
  -F "image_file=@image1.jpg" \
  -F "image_type=image1"
```

## Models

### ImageSet
- `user`: Foreign key to User
- `title`: Optional title for the set
- `description`: Optional description
- `created_at`: Timestamp when created
- `updated_at`: Timestamp when last updated

### Image
- `image_set`: Foreign key to ImageSet
- `image_type`: One of 'image1', 'image2', 'image3'
- `image_file`: The actual image file
- `uploaded_at`: Timestamp when uploaded

## File Structure

```
beepdata_backend/
├── manage.py
├── requirements.txt
├── env.example
├── beepdata_backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── images/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── urls.py
    ├── admin.py
    └── apps.py
```
# DataHub
