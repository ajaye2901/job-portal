from django.urls import path
from .views import *

urlpatterns = [
    path('superuser/login/', AdminLoginView.as_view(), name='admin-login'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='signin'),

    path('superuser/alljobs/', AdminAllJobsView.as_view(), name='all-jobs'),
    path('superuser/delete-job/<int:job_id>/', AdminDeleteJobsView.as_view(), name='delete-jobs'),
    path('superuser/job-applications/', AdminJobApplicationsView.as_view(), name='job-applications'),
    path('superuser/delete-application/<int:application_id>/', AdminJobApplicationsView.as_view(), name='delete-jobapplications'),
    path('superuser/allusers/', AllUsersView.as_view(), name='allusers'),
    
]