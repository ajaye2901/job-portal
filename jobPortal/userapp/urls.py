from django.urls import path
from .views import AdminLoginView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('superuser/login/', AdminLoginView.as_view(), name='admin-login'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='signin'),
]