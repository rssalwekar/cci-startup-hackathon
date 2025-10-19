from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, help_text="Tell us about yourself")
    avatar_url = models.URLField(blank=True, help_text="Profile picture URL from Supabase")
    location = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    preferred_language = models.CharField(max_length=20, default='python')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Statistics
    total_interviews = models.IntegerField(default=0)
    total_problems_solved = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def update_statistics(self):
        """Update profile statistics based on completed interviews"""
        completed_sessions = InterviewSession.objects.filter(
            user=self.user,
            status='completed'
        )
        
        self.total_interviews = completed_sessions.count()
        
        # Count unique problems solved
        self.total_problems_solved = completed_sessions.filter(
            problem__isnull=False
        ).values('problem').distinct().count()
        
        # Calculate average score
        scores = completed_sessions.filter(
            performance_score__isnull=False
        ).values_list('performance_score', flat=True)
        
        if scores:
            self.average_score = sum(scores) / len(scores)
        
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a new user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')
    difficulty_preference = models.CharField(max_length=10, choices=Problem.DIFFICULTY_CHOICES, null=True, blank=True)
    topic_preferences = models.JSONField(default=list)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)
    
    # Recording fields
    audio_recording_url = models.URLField(blank=True, help_text="URL to audio recording in Supabase")
    video_recording_url = models.URLField(blank=True, help_text="URL to video recording in Supabase")
    screen_recording_url = models.URLField(blank=True, help_text="URL to screen recording in Supabase")
    recording_duration = models.IntegerField(default=0, help_text="Recording duration in seconds")
    
    # Performance metrics
    performance_score = models.FloatField(null=True, blank=True, help_text="Overall performance score (0-100)")
    code_quality_score = models.FloatField(null=True, blank=True, help_text="Code quality score (0-100)")
    communication_score = models.FloatField(null=True, blank=True, help_text="Communication score (0-100)")
    problem_solving_score = models.FloatField(null=True, blank=True, help_text="Problem solving score (0-100)")
    
    def __str__(self):
        return f"Interview {self.id} - {self.user.username}"
    
    def get_duration(self):
        """Calculate interview duration"""
        if self.completed_at and self.started_at:
            duration = self.completed_at - self.started_at
            return duration.total_seconds() / 60  # Return minutes
        return 0
    
    def has_recordings(self):
        """Check if session has any recordings"""
        return bool(self.audio_recording_url or self.video_recording_url or self.screen_recording_url)


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
