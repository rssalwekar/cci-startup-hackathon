from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    # LeetCode specific fields
    leetcode_id = models.IntegerField(unique=True, null=True, blank=True)  # LeetCode problem number
    title_slug = models.CharField(max_length=200, unique=True, null=True, blank=True)  # LeetCode title slug
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    topics = models.JSONField(default=list)  # List of topics like ['arrays', 'two-pointers']
    constraints = models.TextField(blank=True)
    examples = models.JSONField(default=list)  # List of input/output examples
    hints = models.JSONField(default=list)  # Progressive hints for the problem
    function_signature = models.TextField(blank=True)  # Generated function signature
    test_cases = models.JSONField(default=list)  # Generated test cases
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class InterviewSession(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')
    difficulty_preference = models.CharField(max_length=10, choices=Problem.DIFFICULTY_CHOICES, null=True, blank=True)
    topic_preferences = models.JSONField(default=list)
    problem_name_request = models.CharField(max_length=200, blank=True)  # Store specific problem name requests
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)
    
    def __str__(self):
        return f"Interview {self.id} - {self.user.username}"


class ChatMessage(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."


class CodeSubmission(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='code_submissions')
    code = models.TextField()
    language = models.CharField(max_length=20, default='python')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_solution = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Code submission {self.id} for session {self.session.id}"


class UserProblem(models.Model):
    """Track which problems each user has already been given to avoid repetition"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'problem']  # Prevent duplicate assignments
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"


class InterviewRecording(models.Model):
    """Store interview session recordings and metadata"""
    session = models.OneToOneField(InterviewSession, on_delete=models.CASCADE, related_name='recording')
    video_file = models.FileField(upload_to='interview_recordings/', null=True, blank=True)
    audio_file = models.FileField(upload_to='interview_recordings/', null=True, blank=True)
    screen_recording = models.FileField(upload_to='interview_recordings/', null=True, blank=True)
    recording_started_at = models.DateTimeField(auto_now_add=True)
    recording_ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"Recording for session {self.session.id}"
