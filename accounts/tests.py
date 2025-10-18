# Tests for Accounts App
from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserSession
from django.urls import reverse


class UserAuthenticationTests(TestCase):
    """Test user authentication functionality"""
    
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        
    def test_signup_page_loads(self):
        """Test that signup page loads successfully"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Your Account')
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_user_profile_requires_login(self):
        """Test that profile page requires authentication"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login


class UserProfileTests(TestCase):
    """Test user profile functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            years_of_experience=3,
            target_companies='Google, Amazon',
            preferred_languages='Python, JavaScript'
        )
    
    def test_profile_creation(self):
        """Test that user profile is created correctly"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.years_of_experience, 3)
    
    def test_get_target_companies_list(self):
        """Test parsing target companies"""
        companies = self.profile.get_target_companies_list()
        self.assertEqual(len(companies), 2)
        self.assertIn('Google', companies)
        self.assertIn('Amazon', companies)
    
    def test_get_preferred_languages_list(self):
        """Test parsing preferred languages"""
        languages = self.profile.get_preferred_languages_list()
        self.assertEqual(len(languages), 2)
        self.assertIn('Python', languages)
        self.assertIn('JavaScript', languages)
