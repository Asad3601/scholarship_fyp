from django.urls import path
from . import views

urlpatterns = [
    # path('scholarship_ads/', views.scholarships_ads, name='scholarship_ads'),
    path('scholarships/', views.scholarships_data, name='scholarships'),
    path('scholarships_portal/', views.scholarships_portal, name='scholarships_portal'),
    path('ads/', views.scholarships_ads, name='ads'),
    path('<str:title>/', views.get_scholarship_by_title,),
    path('filter/', views.scholarships_filter, name='filter')
]
