from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Interview(models.Model):
    """
    Model to store interview sessions
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
    title = models.CharField(max_length=255)
    problem_name = models.CharField(max_length=255)
    problem_description = models.TextField()
    problem_difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    problem_link = models.URLField(blank=True, null=True, help_text="Link to LeetCode or similar")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Interview timing
    scheduled_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=45)
    
    # Recording and transcript
    recording_url = models.URLField(blank=True, null=True, help_text="Supabase storage URL")
    recording_path = models.CharField(max_length=500, blank=True, null=True, help_text="Path in Supabase storage")
    transcript = models.TextField(blank=True, null=True)
    
    # Code submission
    submitted_code = models.TextField(blank=True, null=True)
    programming_language = models.CharField(max_length=50, default='python')
    
    # AI feedback and scoring
    overall_score = models.IntegerField(null=True, blank=True, help_text="Score out of 100")
    communication_score = models.IntegerField(null=True, blank=True, help_text="Score out of 100")
    problem_solving_score = models.IntegerField(null=True, blank=True, help_text="Score out of 100")
    code_quality_score = models.IntegerField(null=True, blank=True, help_text="Score out of 100")
    
    feedback_report = models.TextField(blank=True, null=True, help_text="Detailed AI-generated feedback")
    strengths = models.TextField(blank=True, null=True, help_text="What went well")
    areas_for_improvement = models.TextField(blank=True, null=True, help_text="What can be improved")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.problem_name} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def get_duration_display(self):
        """Return formatted duration"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes} minutes"
        return f"{self.duration_minutes} minutes (scheduled)"
    
    def is_completed(self):
        """Check if interview is completed"""
        return self.status == 'completed'


class InterviewNote(models.Model):
    """
    Notes and observations during the interview
    """
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='notes')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    note_type = models.CharField(
        max_length=50,
        choices=[
            ('observation', 'Observation'),
            ('hint_given', 'Hint Given'),
            ('question_asked', 'Question Asked'),
            ('code_change', 'Code Change'),
        ],
        default='observation'
    )
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Note for {self.interview.problem_name} at {self.timestamp}"


class InterviewFeedbackPoint(models.Model):
    """
    Individual feedback points for an interview
    """
    CATEGORY_CHOICES = [
        ('communication', 'Communication'),
        ('problem_solving', 'Problem Solving'),
        ('code_quality', 'Code Quality'),
        ('testing', 'Testing'),
        ('time_management', 'Time Management'),
        ('clarification', 'Clarification'),
    ]
    
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='feedback_points')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_positive = models.BooleanField(default=True, help_text="True for strength, False for improvement area")
    point = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', '-is_positive']
    
    def __str__(self):
        feedback_type = "Strength" if self.is_positive else "Improvement"
        return f"{self.category} - {feedback_type}"
