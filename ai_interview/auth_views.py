"""
Authentication and user profile views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import UserProfile, InterviewSession
from .supabase_service import supabase_service
import json


def custom_logout(request):
    """Custom logout view that handles both GET and POST"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


def signup(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('start_interview')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists')
        
        if not email:
            errors.append('Email is required')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already exists')
        
        if not password:
            errors.append('Password is required')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        
        if password != password_confirm:
            errors.append('Passwords do not match')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'registration/signup.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to AI Coding Interview.')
            return redirect('start_interview')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'registration/signup.html')
    
    return render(request, 'registration/signup.html')


@login_required
def profile(request):
    """User profile view showing user info and statistics"""
    user = request.user
    profile = user.profile
    
    # Update statistics
    profile.update_statistics()
    
    # Get recent interviews
    recent_interviews = InterviewSession.objects.filter(
        user=user,
        status='completed'
    ).order_by('-completed_at')[:5]
    
    # Get interview statistics
    total_time = sum(
        session.get_duration() 
        for session in InterviewSession.objects.filter(user=user, status='completed')
    )
    
    context = {
        'profile': profile,
        'recent_interviews': recent_interviews,
        'total_time_minutes': int(total_time),
    }
    
    return render(request, 'ai_interview/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        
        # Update profile info
        profile.bio = request.POST.get('bio', '').strip()
        profile.location = request.POST.get('location', '').strip()
        profile.github_url = request.POST.get('github_url', '').strip()
        profile.linkedin_url = request.POST.get('linkedin_url', '').strip()
        profile.website_url = request.POST.get('website_url', '').strip()
        profile.preferred_language = request.POST.get('preferred_language', 'python')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'profile': profile,
        'languages': ['python', 'javascript', 'java', 'c++', 'go', 'rust']
    }
    
    return render(request, 'ai_interview/edit_profile.html', context)


@login_required
@require_http_methods(["POST"])
def upload_avatar(request):
    """Upload user avatar to Supabase"""
    try:
        if 'avatar' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)
        
        avatar_file = request.FILES['avatar']
        
        # Validate file size (max 5MB)
        if avatar_file.size > 5 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': 'File too large (max 5MB)'}, status=400)
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if avatar_file.content_type not in allowed_types:
            return JsonResponse({'success': False, 'error': 'Invalid file type'}, status=400)
        
        # Read file data
        file_data = avatar_file.read()
        
        # Upload to Supabase
        success, public_url = supabase_service.upload_avatar(
            file_data,
            request.user.id,
            avatar_file.name
        )
        
        if success and public_url:
            # Update profile with new avatar URL
            profile = request.user.profile
            profile.avatar_url = public_url
            profile.save()
            
            return JsonResponse({
                'success': True,
                'avatar_url': public_url
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to upload avatar'
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def interview_history(request):
    """Display all past interviews with filtering and pagination"""
    user = request.user
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    difficulty_filter = request.GET.get('difficulty', 'all')
    search_query = request.GET.get('q', '')
    
    # Build query
    interviews = InterviewSession.objects.filter(user=user)
    
    if status_filter != 'all':
        interviews = interviews.filter(status=status_filter)
    
    if difficulty_filter != 'all':
        interviews = interviews.filter(difficulty_preference=difficulty_filter)
    
    if search_query:
        interviews = interviews.filter(
            Q(problem__title__icontains=search_query) |
            Q(problem__description__icontains=search_query)
        )
    
    # Order by most recent
    interviews = interviews.order_by('-started_at')
    
    # Pagination
    paginator = Paginator(interviews, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Calculate statistics
    completed_interviews = InterviewSession.objects.filter(user=user, status='completed')
    avg_score = completed_interviews.aggregate(Avg('performance_score'))['performance_score__avg'] or 0
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'difficulty_filter': difficulty_filter,
        'search_query': search_query,
        'total_interviews': interviews.count(),
        'avg_score': round(avg_score, 1) if avg_score else 0,
    }
    
    return render(request, 'ai_interview/history.html', context)


@login_required
def interview_detail(request, session_id):
    """View details of a specific interview session - shows the same results page as after completion"""
    session = get_object_or_404(
        InterviewSession,
        id=session_id,
        user=request.user
    )
    
    # Get messages and code submissions
    messages = session.messages.all().order_by('timestamp')
    code_submissions = session.code_submissions.all().order_by('timestamp')
    
    # Try to get recording data
    try:
        recording = session.recording
    except:
        recording = None
    
    context = {
        'session': session,
        'messages': messages,
        'code_submissions': code_submissions,
        'recording': recording,
    }
    
    # Use the same results template that's shown after completing an interview
    return render(request, 'ai_interview/results.html', context)


@login_required
@require_http_methods(["POST"])
def delete_interview(request, session_id):
    """Delete an interview session"""
    try:
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )
        
        # Delete associated recordings from Supabase
        # (Optional: implement this if you want to delete files from storage)
        
        session.delete()
        messages.success(request, 'Interview deleted successfully')
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
