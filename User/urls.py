from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.add_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('data/', views.user_data, name='data'),
    path('profile/', views.profile, name='profile'),
    path('save_scholarship/', views.save_scholarship, name='save_scholarship'),
    path('saved/', views.saved, name='saved'),
    path('del_scholarship/<int:id>/',views.del_scholarship,name="del_scholarship"),
]
