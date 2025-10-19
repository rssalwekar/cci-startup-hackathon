from django.contrib import admin
from .models import Problem, InterviewSession, ChatMessage, CodeSubmission, UserProblem, InterviewRecording


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


@admin.register(InterviewRecording)
class InterviewRecordingAdmin(admin.ModelAdmin):
    list_display = ['session', 'recording_started_at', 'duration_seconds']
    list_filter = ['recording_started_at']
    search_fields = ['session__user__username']
    readonly_fields = ['recording_started_at', 'recording_ended_at']
