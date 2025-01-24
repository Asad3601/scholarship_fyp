from django.urls import path
from . import views

urlpatterns = [
    path('scholarship_ads/', views.scholarships_ads, name='scholarship_ads'),
    path('scholarships/', views.scholarships_data, name='scholarships'),
    path('masters_portal/', views.masters_portal, name='masters_portal'),
]
