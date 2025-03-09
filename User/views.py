from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from .models import UserModel,SavedSchaolarship
from Scholarship.models import Scholarship
import bcrypt
import os
from User.validations import *
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta
from User.context_processors import jwt_user_data
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def add_user(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        # Validate first name
        first_name_error = validate_name(first_name)
        if first_name_error:
            return JsonResponse({'field': 'first_name', 'error': f"first {first_name_error}"}, status=400)

        # Validate last name
        last_name_error = validate_name(last_name)
        if last_name_error:
            return JsonResponse({'field': 'last_name', 'error': f"last {last_name_error}"}, status=400)

        # Check if the email already exists
        if UserModel.objects.filter(email=email).exists():
            return JsonResponse({'field': 'email', 'error': 'email already exists'}, status=400)

        # Validate passwords
        if password1 != password2:
            return JsonResponse({'field': 'password2', 'error': 'passwords do not match'}, status=400)
        else:
            password_error = validate_password(password1)
            if password_error:
                return JsonResponse({'field': 'password1', 'error': password_error}, status=400)

        # Encrypt the password using bcrypt
        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create a new user
        user = UserModel.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )

        return JsonResponse({'message': 'User Created Successfully', 'user_id': user.id}, status=201)

    return render(request, 'user/register.html')






from django.http import JsonResponse
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from .models import UserModel

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find the user by email
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return JsonResponse({'field': 'email', 'error': 'This email address not exist'}, status=401)

        # Match the password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({'field': 'password', 'error': 'Invalid email or password'}, status=401)

        # Generate JWT token
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

        return JsonResponse({'message': 'Login Successful', 'jwt_token': token}, status=200)

    return render(request, 'User/login.html')  # Render a login form if the method is GET





@jwt_required
def user_data(request):
    context = jwt_user_data(request)
   
    user_data = context.get('user_data', None)
    return JsonResponse({"user_data": user_data})
@jwt_required
def profile(request):
    return render (request,'user/profile.html') 





@jwt_required
@csrf_exempt
def save_scholarship(request):
    context = jwt_user_data(request)
    user_data = context.get('user_data', None)

    if request.method == "POST":
        title = request.POST.get("title")
        degrees = request.POST.get("degrees")
        description = request.POST.get("description")
        location = request.POST.get("location")
        due_date = request.POST.get("due_date")
        link = request.POST.get("link")

        # Check if scholarship is already saved by this user
        existing_scholarship = SavedSchaolarship.objects.filter(
            user_id=user_data["id"], title=title
        ).exists()

        if existing_scholarship:
            return JsonResponse({"duplicate": True, "message": "Scholarship already saved!"})

        # Save new scholarship
        SavedSchaolarship.objects.create(
            user_id=user_data["id"],
            title=title,
            degrees=degrees,
            description=description,
            location=location,
            due_date=due_date,
            link=link
        )

        return JsonResponse({"duplicate": False, "message": "Scholarship saved successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)



@jwt_required
def saved(request):
    print("Save scholarships")
    context = jwt_user_data(request)
    user_data = context.get('user_data', None)
    if user_data['id']:
        user_id = user_data['id']
        
        # Query the SavedJob model to get saved jobs of the logged-in user
        saved_schoalrships = SavedSchaolarship.objects.filter(user=user_id)

        return render(request, 'user/saved_schoalrships.html', {'saved_schoalrships': saved_schoalrships})
    else:
        # Handle the case where the user is not authenticated
        # You might want to redirect them to a login page or show a message
        return redirect('login')

@jwt_required
def del_scholarship(request,id):
    scholarship = SavedSchaolarship.objects.get(id=id)
    scholarship.delete()
    return redirect('saved')
