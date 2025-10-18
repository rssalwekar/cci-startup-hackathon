from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, UserSession
from .forms import SignUpForm, LoginForm, UserProfileForm
from .supabase_client import sign_up_user, sign_in_user, sign_out_user
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Home page"""
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'accounts/home.html')


def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                # Create user in Django
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                
                # Create user in Supabase
                supabase_response = sign_up_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    metadata={
                        'username': form.cleaned_data['username'],
                        'first_name': form.cleaned_data.get('first_name', ''),
                        'last_name': form.cleaned_data.get('last_name', ''),
                    }
                )
                
                # Create user profile
                profile = UserProfile.objects.create(user=user)
                
                if supabase_response.get('success'):
                    # Store Supabase user ID
                    supabase_user = supabase_response.get('user')
                    if supabase_user:
                        profile.supabase_user_id = supabase_user.id
                        profile.save()
                    
                    # Create session if available
                    session_data = supabase_response.get('session')
                    if session_data:
                        UserSession.objects.create(
                            user=user,
                            supabase_session_token=session_data.access_token,
                            refresh_token=session_data.refresh_token if hasattr(session_data, 'refresh_token') else '',
                            expires_at=timezone.now() + timedelta(hours=24)
                        )
                
                # Log the user in
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('profile')
                
            except Exception as e:
                logger.error(f"Error during signup: {str(e)}")
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Authenticate with Supabase
                supabase_response = sign_in_user(email, password)
                
                if supabase_response.get('success'):
                    # Find Django user by email
                    try:
                        user = User.objects.get(email=email)
                        
                        # Update or create session
                        session_data = supabase_response.get('session')
                        if session_data:
                            # Deactivate old sessions
                            UserSession.objects.filter(user=user, is_active=True).update(is_active=False)
                            
                            # Create new session
                            UserSession.objects.create(
                                user=user,
                                supabase_session_token=session_data.access_token,
                                refresh_token=session_data.refresh_token if hasattr(session_data, 'refresh_token') else '',
                                expires_at=timezone.now() + timedelta(hours=24)
                            )
                        
                        # Log user in to Django
                        login(request, user)
                        messages.success(request, 'Logged in successfully!')
                        
                        # Redirect to next page or profile
                        next_url = request.GET.get('next', 'profile')
                        return redirect(next_url)
                        
                    except User.DoesNotExist:
                        messages.error(request, 'User account not found. Please sign up first.')
                else:
                    messages.error(request, 'Invalid email or password')
                    
            except Exception as e:
                logger.error(f"Error during login: {str(e)}")
                messages.error(request, f'Login error: {str(e)}')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Handle user logout"""
    try:
        # Get active session
        active_session = UserSession.objects.filter(
            user=request.user,
            is_active=True
        ).first()
        
        if active_session:
            # Sign out from Supabase
            sign_out_user(active_session.supabase_session_token)
            
            # Deactivate session
            active_session.is_active = False
            active_session.save()
        
        # Logout from Django
        logout(request)
        messages.success(request, 'Logged out successfully!')
        
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        logout(request)
    
    return redirect('home')


@login_required
def profile_view(request):
    """Display user profile with interview history"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Get interview history (will be populated by interviews app)
    from interviews.models import Interview
    
    # Get all interviews for statistics (before slicing)
    all_interviews = Interview.objects.filter(user=request.user)
    completed_interviews = all_interviews.filter(status='completed')
    
    # Calculate statistics
    total_interviews = all_interviews.count()
    completed_count = completed_interviews.count()
    
    # Calculate average score
    avg_score = 0
    if completed_count > 0:
        scores = [i.overall_score for i in completed_interviews if i.overall_score is not None]
        if scores:
            avg_score = sum(scores) / len(scores)
    
    # Get recent interviews for display (after calculating stats)
    recent_interviews = all_interviews.order_by('-created_at')[:10]
    
    context = {
        'profile': profile,
        'interviews': recent_interviews,
        'total_interviews': total_interviews,
        'completed_count': completed_count,
        'avg_score': round(avg_score, 1) if avg_score else 0,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            # Update user fields
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()
            
            # Save profile
            form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
