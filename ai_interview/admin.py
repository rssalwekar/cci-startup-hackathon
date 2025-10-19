from django.contrib import admin
from .models import Problem, InterviewSession, ChatMessage, CodeSubmission, UserProblem, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'preferred_language', 'total_interviews', 'average_score']
    list_filter = ['preferred_language', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at', 'total_interviews', 'total_problems_solved', 'average_score']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'topics', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'difficulty_preference', 'started_at']
    list_filter = ['status', 'difficulty_preference', 'started_at']
    search_fields = ['user__username']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'message_type', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp']


@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'language', 'timestamp', 'is_solution']
    list_filter = ['language', 'is_solution', 'timestamp']
    search_fields = ['code']
    readonly_fields = ['timestamp']


@admin.register(UserProblem)
class UserProblemAdmin(admin.ModelAdmin):
    list_display = ['user', 'problem', 'assigned_at', 'session']
    list_filter = ['assigned_at', 'problem__difficulty']
    search_fields = ['user__username', 'problem__title']
    readonly_fields = ['assigned_at']
