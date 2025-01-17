import re,os
import jwt
from django.http import JsonResponse
from functools import wraps
from .context_processors import jwt_user_data
from django.shortcuts import render, redirect

def validate_password(password):
    """
    Validate password with the following rules:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    - Length between 6 and 8 characters
    """
    if len(password) < 6 or len(password) > 8:
        return "Password must be 6 to 8 characters long."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."
    return None

def validate_name(name):
    """
    Validate that the name contains only alphabetic characters and spaces.
    - No numbers or special characters allowed.
    """
    if not re.match(r'^[A-Za-z\s]+$', name):
        return "name must contain only letters and spaces."
    return None








def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if `jwt_token` exists in cookies
        token = request.COOKIES.get('jwt_token')
        if token:
            # If token exists, proceed with the view without decoding the token
            return view_func(request, *args, **kwargs)
        
        # Check if `user_data` exists in context (user_data should be attached to the request object via the context processor)
        context = jwt_user_data(request)
        user_data = context.get('user_data', None)
        if user_data:
            # If user_data exists in context, proceed with the view
            return view_func(request, *args, **kwargs)

        # If neither token in cookies nor user_data in context, redirect to login page
        return redirect('login')  # Replace 'login' with the actual name of your login view URL

    return wrapper
