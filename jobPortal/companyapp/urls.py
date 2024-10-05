from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'joblisting', JobListingView, basename='joblisting')

urlpatterns = [
    path('register/', CompanyCreateView.as_view(), name='company-register'),
    path('all-applications/', AllJobApplicationsView.as_view(), name='all-applications'),
    path('status_change/<int:application_id>/', ApplicationStatusChangeView.as_view(), name='status-change'),
    path('', include(router.urls)),
]