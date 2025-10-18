from django.contrib import admin
from .models import Interview, InterviewNote, InterviewFeedbackPoint


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem_name', 'problem_difficulty', 'status', 
                    'overall_score', 'created_at')
    list_filter = ('status', 'problem_difficulty', 'programming_language', 'created_at')
    search_fields = ('user__username', 'problem_name', 'title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'status')
        }),
        ('Problem Details', {
            'fields': ('problem_name', 'problem_description', 'problem_difficulty', 
                      'problem_link', 'programming_language')
        }),
        ('Timing', {
            'fields': ('scheduled_at', 'started_at', 'completed_at', 'duration_minutes')
        }),
        ('Recording & Code', {
            'fields': ('recording_url', 'recording_path', 'transcript', 'submitted_code')
        }),
        ('Scores & Feedback', {
            'fields': ('overall_score', 'communication_score', 'problem_solving_score',
                      'code_quality_score', 'feedback_report', 'strengths', 
                      'areas_for_improvement')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(InterviewNote)
class InterviewNoteAdmin(admin.ModelAdmin):
    list_display = ('interview', 'note_type', 'timestamp')
    list_filter = ('note_type', 'timestamp')
    search_fields = ('interview__problem_name', 'content')


@admin.register(InterviewFeedbackPoint)
class InterviewFeedbackPointAdmin(admin.ModelAdmin):
    list_display = ('interview', 'category', 'is_positive', 'created_at')
    list_filter = ('category', 'is_positive', 'created_at')
    search_fields = ('interview__problem_name', 'point')
