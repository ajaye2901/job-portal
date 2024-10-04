from django.urls import path
from .views import CompanyCreateView

urlpatterns = [
    path('register/', CompanyCreateView.as_view(), name='company-register'),
]