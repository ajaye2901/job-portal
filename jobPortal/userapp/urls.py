from django.urls import path
from .views import AdminLoginView

urlpatterns = [
    path('superuser/login/', AdminLoginView.as_view(), name='admin-login'),
]