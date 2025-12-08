from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.company_home, name='company_home'),
    path('about/', views.company_about, name='company_about'),
]
