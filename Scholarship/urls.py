from django.urls import path
from . import views

urlpatterns = [
    # path('scholarship_ads/', views.scholarships_ads, name='scholarship_ads'),
    path('scholarships/', views.scholarships_data, name='scholarships'),
    path('wemake/', views.wemakescholars_portal, name='wemake'),
    path('masters_portal/', views.masters_portal, name='masters_portal'),
    path('scholarships_portal/', views.scholarships_portal, name='scholarships_portal'),
    path('ads/', views.scholarships_ads, name='ads'),
]
