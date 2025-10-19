from django.db import models


class InterviewReport(models.Model):
    """
    Stores generated reports
    Links to interview session (created by other team member)
    """
    
    # Foreign key to existing interview session
    session_id = models.IntegerField(unique=True)
    
    # Overall Scores
    overall_score = models.FloatField()
    code_quality_score = models.FloatField()
    communication_score = models.FloatField()
    problem_solving_score = models.FloatField()
    time_management_score = models.FloatField()
    
    # Detailed Analysis (stored as JSON)
    code_analysis = models.JSONField()
    communication_analysis = models.JSONField()
    strengths = models.JSONField()
    weaknesses = models.JSONField()
    improvement_tips = models.JSONField()
    recommended_resources = models.JSONField()
    
    # AI Generated Feedback 
    detailed_feedback = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        db_table = 'interview_reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report for session {self.session_id}" 
        