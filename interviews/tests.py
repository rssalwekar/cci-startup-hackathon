# Tests for Interviews App
from django.test import TestCase, Client
from django.contrib.auth.models import User
from interviews.models import Interview, InterviewNote, InterviewFeedbackPoint
from django.urls import reverse
from django.utils import timezone


class InterviewModelTests(TestCase):
    """Test Interview model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.interview = Interview.objects.create(
            user=self.user,
            title='Test Interview',
            problem_name='Two Sum',
            problem_description='Find two numbers that add up to target',
            problem_difficulty='easy',
            programming_language='python',
            status='scheduled'
        )
    
    def test_interview_creation(self):
        """Test that interview is created correctly"""
        self.assertEqual(self.interview.user.username, 'testuser')
        self.assertEqual(self.interview.problem_name, 'Two Sum')
        self.assertEqual(self.interview.status, 'scheduled')
    
    def test_interview_str_representation(self):
        """Test string representation of interview"""
        expected = f"testuser - Two Sum ({self.interview.created_at.strftime('%Y-%m-%d')})"
        self.assertEqual(str(self.interview), expected)
    
    def test_is_completed(self):
        """Test is_completed method"""
        self.assertFalse(self.interview.is_completed())
        self.interview.status = 'completed'
        self.assertTrue(self.interview.is_completed())


class InterviewViewTests(TestCase):
    """Test Interview views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.interview = Interview.objects.create(
            user=self.user,
            title='Test Interview',
            problem_name='Two Sum',
            problem_description='Test description',
            problem_difficulty='medium',
            programming_language='python'
        )
        self.list_url = reverse('interview_list')
        self.detail_url = reverse('interview_detail', args=[self.interview.id])
        self.create_url = reverse('create_interview')
    
    def test_interview_list_requires_login(self):
        """Test that interview list requires authentication"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
    
    def test_interview_list_shows_user_interviews(self):
        """Test that interview list shows user's interviews"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Two Sum')
    
    def test_interview_detail_requires_login(self):
        """Test that interview detail requires authentication"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 302)
    
    def test_interview_detail_shows_problem(self):
        """Test that interview detail shows problem information"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Two Sum')


class InterviewFeedbackTests(TestCase):
    """Test Interview feedback functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.interview = Interview.objects.create(
            user=self.user,
            title='Test Interview',
            problem_name='Two Sum',
            problem_description='Test description',
            status='completed',
            overall_score=85,
            communication_score=90,
            problem_solving_score=82,
            code_quality_score=83
        )
        self.feedback_point = InterviewFeedbackPoint.objects.create(
            interview=self.interview,
            category='communication',
            is_positive=True,
            point='Good explanation of approach'
        )
    
    def test_feedback_point_creation(self):
        """Test that feedback point is created correctly"""
        self.assertEqual(self.feedback_point.interview, self.interview)
        self.assertEqual(self.feedback_point.category, 'communication')
        self.assertTrue(self.feedback_point.is_positive)
    
    def test_interview_scores(self):
        """Test that interview scores are saved correctly"""
        self.assertEqual(self.interview.overall_score, 85)
        self.assertEqual(self.interview.communication_score, 90)
        self.assertEqual(self.interview.problem_solving_score, 82)
        self.assertEqual(self.interview.code_quality_score, 83)


class InterviewNoteTests(TestCase):
    """Test Interview notes functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.interview = Interview.objects.create(
            user=self.user,
            title='Test Interview',
            problem_name='Two Sum',
            problem_description='Test description'
        )
        self.note = InterviewNote.objects.create(
            interview=self.interview,
            content='User asked clarifying question',
            note_type='question_asked'
        )
    
    def test_note_creation(self):
        """Test that note is created correctly"""
        self.assertEqual(self.note.interview, self.interview)
        self.assertEqual(self.note.content, 'User asked clarifying question')
        self.assertEqual(self.note.note_type, 'question_asked')
