from django.urls import path
from Scholarship.views import scholarships_get,scholarships_data,scholarships_portal,get_scholarship_by_title

urlpatterns = [
    # path('scholarship_ads/', views.scholarships_ads, name='scholarship_ads'),
    path('filter/', scholarships_get),
    path('scholarships/', scholarships_data, name='scholarships'),
    path('scholarships_portal/', scholarships_portal, name='scholarships_portal'),
    path('<str:title>/', get_scholarship_by_title),
]
