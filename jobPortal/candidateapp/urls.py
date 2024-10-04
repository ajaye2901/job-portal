from django.urls import path, include
from .views import *

urlpatterns = [
    path('jobapply/', JobApplicationView.as_view(), name='jobapply'),
    path('alljobs/', AllJobsView.as_view(), name='alljobs'),
    path('job-detailed/<int:job_id>/', JobDetailedView.as_view(), name='job-detailed'),
    path('job-applications/', AllJobApplicationView.as_view(), name='job-applications'),
]