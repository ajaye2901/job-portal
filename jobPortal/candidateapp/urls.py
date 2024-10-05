from django.urls import path, include
from .views import *

urlpatterns = [
    path('jobapply/', JobApplicationView.as_view(), name='jobapply'),
    path('alljobs/', AllJobsView.as_view(), name='alljobs'),
    path('job-detailed/<int:job_id>/', JobDetailedView.as_view(), name='job-detailed'),
    path('job-applications/', AllJobApplicationView.as_view(), name='job-applications'),
    path('detailed-application/<int:application_id>/', JobApplicationDetailedview.as_view(), name='detailed-application'),
    path('delete-jobapplication/<int:application_id>/', JobApplicationDeleteView.as_view(), name='delete-jobapplication'),
    path('jobs/', JobListingFilterView.as_view(), name='job-filter')    
]