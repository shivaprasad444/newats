"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("", views.home, name="home"),
    path("login/",  views.login_view,  name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/profile/", views.profile, name="profile"),
    path("dashboard/jobs/", views.jobs_applied,name="jobs_applied"),
    path("dashboard/interviews/",views.interviews,name="interviews"),
    path("dashboard/calendar/", views.calendar,name="calendar"),
    path("candidate/signup/", views.candidate_signup_view, name="candidate-signup"),
    path("company/signup/", views.company_signup, name="company_signup"),
    path("job/<int:pk>/", views.job_detail_view, name="job_detail"),
    path('candidate/timesheet/', views.candidate_timesheet_view, name='candidate_timesheet'),
    path('contact/', views.contact_us_view, name='contact_us'),


]
