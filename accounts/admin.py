from django.contrib import admin
from .models import UserProfile, UserSession


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'years_of_experience', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'supabase_user_id')
    list_filter = ('years_of_experience', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'expires_at', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at',)
