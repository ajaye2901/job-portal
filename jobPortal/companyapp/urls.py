from django.urls import path, include
from .views import CompanyCreateView, JobListingView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'joblisting', JobListingView, basename='joblisting')

urlpatterns = [
    path('register/', CompanyCreateView.as_view(), name='company-register'),
    path('', include(router.urls)),
]