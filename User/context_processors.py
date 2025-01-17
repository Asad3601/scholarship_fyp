import jwt
import os
from django.conf import settings
from .models import UserModel


def jwt_user_data(request):
    """
    Decodes JWT token from request cookies and adds user data to context.
    """
    user_data = None
    token = request.COOKIES.get('jwt_token')  # The token should be in cookies

    if token:
        try:
            # Decode JWT token (you should verify signature in production)
            decoded_data = jwt.decode(token, os.getenv('SECRET_KEY', 'your_default_secret'), algorithms=["HS256"])
            
            # Check if 'user_id' exists in the decoded token
            if 'user_id' in decoded_data:
                try:
                    # Attempt to retrieve the user from the database
                    user = UserModel.objects.get(id=decoded_data['user_id'])
                    user_data = {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'created_at': user.created_at,
                        'updated_at': user.updated_at
                    }
                    print("Logged in username:", user_data['first_name'])
                except UserModel.DoesNotExist:
                    print("User with given ID does not exist")
                    user_data = None
            else:
                print("No user_id in decoded token")
                user_data = None
        
        except jwt.ExpiredSignatureError:
            print("JWT token has expired")
            user_data = None  # Token expired
        except jwt.InvalidTokenError:
            print("Invalid JWT token")
            user_data = None  # Invalid token
    else:
        print("No JWT token found in cookies")

    if not user_data:
        print("Not any user logged in")

    # Attach user data to the request object so it's available throughout the request-response cycle
    request.user_data=user_data
    

    return {'user_data': user_data}
