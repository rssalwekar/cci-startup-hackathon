"""
URL configuration for interview_platform project.

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from ai_interview import auth_views as custom_auth_views
from ai_interview import views as interview_views

def home_redirect(request):
    # Keep the redirect helper for backwards compatibility
    return interview_views.home(request)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", interview_views.home, name='home'),
    path("ai-interview/", include('ai_interview.urls')),
    
    # Authentication
    path("accounts/login/", auth_views.LoginView.as_view(), name='login'),
    path("accounts/logout/", custom_auth_views.custom_logout, name='logout'),
    path("accounts/signup/", custom_auth_views.signup, name='signup'),
    
    # Profile routes at root level for better UX
    path("profile/", custom_auth_views.profile, name='profile'),
    path("profile/edit/", custom_auth_views.edit_profile, name='edit_profile'),
    path("profile/upload-avatar/", custom_auth_views.upload_avatar, name='upload_avatar'),
    path("history/", custom_auth_views.interview_history, name='interview_history'),
    path("history/<int:session_id>/", custom_auth_views.interview_detail, name='interview_detail'),
    path("history/<int:session_id>/delete/", custom_auth_views.delete_interview, name='delete_interview'),
]
