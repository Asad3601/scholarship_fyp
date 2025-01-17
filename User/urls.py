from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.add_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('data/', views.user_data, name='data'),
]
