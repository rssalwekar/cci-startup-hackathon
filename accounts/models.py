from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extended user profile with Supabase integration
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    supabase_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    target_companies = models.TextField(blank=True, null=True, help_text="Comma-separated list of target companies")
    preferred_languages = models.TextField(blank=True, null=True, help_text="Comma-separated programming languages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_target_companies_list(self):
        """Return target companies as a list"""
        if self.target_companies:
            return [company.strip() for company in self.target_companies.split(',')]
        return []
    
    def get_preferred_languages_list(self):
        """Return preferred languages as a list"""
        if self.preferred_languages:
            return [lang.strip() for lang in self.preferred_languages.split(',')]
        return []


class UserSession(models.Model):
    """
    Track user sessions with Supabase
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    supabase_session_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Session for {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
