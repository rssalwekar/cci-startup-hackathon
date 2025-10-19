from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
from .models import InterviewSession, ChatMessage, CodeSubmission, Problem, InterviewRecording
from .ai_agent import AIInterviewAgent
from .voice_service import voice_service
from django.contrib.auth import get_user_model


@login_required
def interview_page(request, session_id):
    """Main interview page with chat interface and IDE."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    # Get chat messages for this session
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    
    # Get code submissions
    code_submissions = CodeSubmission.objects.filter(session=session).order_by('timestamp')
    
    context = {
        'session': session,
        'messages': messages,
        'code_submissions': code_submissions,
        'websocket_url': f'ws://{request.get_host()}/ws/interview/{session_id}/'
    }
    
    return render(request, 'ai_interview/interview.html', context)


def home(request):
    """Public home page with CTA to start an interview."""
    # If the user is authenticated, show a CTA to start an interview directly
    start_url = '/accounts/login/?next=/ai-interview/start/'
    if request.user.is_authenticated:
        start_url = '/ai-interview/start/'

    context = {
        'start_url': start_url,
    }
    return render(request, 'ai_interview/home.html', context)


@login_required
def start_interview(request):
    """Start a new interview session."""
    if request.method == 'POST':
        # Create new interview session
        session = InterviewSession.objects.create(
            user=request.user,
            status='preparing'
        )
        return redirect('interview_page', session_id=session.id)
    
    return render(request, 'ai_interview/start_interview.html')


@login_required
def complete_interview(request, session_id):
    """Complete the interview and generate feedback."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Mark session as completed immediately for fast response
            session.status = 'completed'
            session.completed_at = timezone.now()
            session.save()
            
            # Generate AI feedback (this can take time)
            # For better UX, we still do it synchronously but return quickly
            try:
                ai_agent = AIInterviewAgent()
                feedback = ai_agent.generate_feedback(session)
                session.ai_feedback = feedback
                session.save()
            except Exception as feedback_error:
                # If feedback generation fails, log it but don't block completion
                print(f"Error generating feedback: {feedback_error}")
                session.ai_feedback = "Feedback generation in progress. Please refresh the page in a moment."
                session.save()
            
            # Check if this is an AJAX request
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': 'Interview completed successfully'
                })
            else:
                return redirect('interview_results', session_id=session.id)
                
        except Exception as e:
            # Handle errors gracefully
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
            else:
                # For non-AJAX requests, still redirect but log the error
                print(f"Error completing interview: {e}")
                return redirect('interview_results', session_id=session.id)
    
    return render(request, 'ai_interview/complete_interview.html', {'session': session})


@login_required
def interview_results(request, session_id):
    """Display interview results and feedback."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    # Get all messages and code submissions
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    code_submissions = CodeSubmission.objects.filter(session=session).order_by('timestamp')
    
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
    
    return render(request, 'ai_interview/results.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def submit_code(request, session_id):
    """API endpoint for code submission."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        # Save code submission
        CodeSubmission.objects.create(
            session=session,
            code=code,
            language=language
        )
        
        return JsonResponse({'status': 'success'})
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def get_session_data(request, session_id):
    """API endpoint to get session data."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    code_submissions = CodeSubmission.objects.filter(session=session).order_by('timestamp')
    
    data = {
        'session': {
            'id': session.id,
            'status': session.status,
            'difficulty_preference': session.difficulty_preference,
            'topic_preferences': session.topic_preferences,
            'started_at': session.started_at.isoformat(),
            'problem': {
                'id': session.problem.id,
                'title': session.problem.title,
                'description': session.problem.description,
                'difficulty': session.problem.difficulty,
                'constraints': session.problem.constraints,
                'examples': session.problem.examples,
            } if session.problem else None
        },
        'messages': [
            {
                'id': msg.id,
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in messages
        ],
        'code_submissions': [
            {
                'id': sub.id,
                'code': sub.code,
                'language': sub.language,
                'timestamp': sub.timestamp.isoformat()
            }
            for sub in code_submissions
        ]
    }
    
    return JsonResponse(data)


@login_required
def get_test_cases(request, session_id):
    """Get test cases for the current problem in the session."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    if not session.problem:
        return JsonResponse({'test_cases': []})
    
    # Use dynamically generated test cases if available
    test_cases = []
    if session.problem.test_cases:
        try:
            # Handle both string and list formats
            if isinstance(session.problem.test_cases, str):
                test_cases = json.loads(session.problem.test_cases)
            else:
                test_cases = session.problem.test_cases
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    
    # Fallback to examples if no test cases
    if not test_cases and session.problem.examples:
        try:
            # Handle both string and list formats
            if isinstance(session.problem.examples, str):
                examples = json.loads(session.problem.examples)
            else:
                examples = session.problem.examples
                
            for i, example in enumerate(examples):
                if 'input' in example and 'output' in example:
                    test_cases.append({
                        'input': example['input'],
                        'expected': example['output']
                    })
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    
    # If no examples, provide some default test cases based on problem title
    if not test_cases:
        if 'two sum' in session.problem.title.lower():
            test_cases = [
                {'input': 'nums = [2,7,11,15]\ntarget = 9', 'expected': '[0,1]'},
                {'input': 'nums = [3,2,4]\ntarget = 6', 'expected': '[1,2]'},
                {'input': 'nums = [3,3]\ntarget = 6', 'expected': '[0,1]'}
            ]
        elif 'valid parentheses' in session.problem.title.lower():
            test_cases = [
                {'input': 's = "()"', 'expected': 'True'},
                {'input': 's = "()[]{}"', 'expected': 'True'},
                {'input': 's = "(]"', 'expected': 'False'}
            ]
        else:
            # Generic test cases
            test_cases = [
                {'input': 'Test case 1', 'expected': 'Expected output 1'},
                {'input': 'Test case 2', 'expected': 'Expected output 2'}
            ]
    
    return JsonResponse({'test_cases': test_cases})


@login_required
def get_function_signature(request, session_id):
    """Get function signature for the current problem in the session."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    if not session.problem:
        return JsonResponse({'function_signature': ''})
    
    # Return the dynamically generated function signature
    function_signature = session.problem.function_signature or ''
    
    return JsonResponse({'function_signature': function_signature})


@login_required
@require_http_methods(["POST"])
def synthesize_speech(request):
    """Convert text to speech using ElevenLabs API."""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        voice_id = data.get('voice_id', '21m00Tcm4TlvDq8ikWAM')  # Default natural voice
        
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        # Check if we have cached audio
        cache_key = voice_service._create_cache_key(
            voice_service._clean_text_for_speech(text), 
            voice_id
        )
        was_cached = cache_key in voice_service.audio_cache
        
        # Generate speech using ElevenLabs
        audio_base64 = voice_service.generate_speech(text, voice_id)
        
        if audio_base64:
            return JsonResponse({
                'success': True,
                'audio': audio_base64,
                'format': 'mp3',
                'cached': was_cached
            })
        else:
            return JsonResponse({'error': 'Failed to generate speech'}, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_available_voices(request):
    """Get list of available voices from ElevenLabs."""
    try:
        voices = voice_service.get_available_voices()
        return JsonResponse({
            'success': True,
            'voices': voices,
            'service_available': voice_service.is_available()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def get_last_ai_message(request, session_id):
    """Get the last AI message from a session for re-speaking."""
    try:
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        
        # Get the last AI message from the session
        last_message = ChatMessage.objects.filter(
            session=session,
            message_type='ai'
        ).order_by('-timestamp').first()
        
        if last_message:
            return JsonResponse({
                'success': True,
                'message': last_message.content,
                'timestamp': last_message.timestamp.isoformat()
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No AI messages found in this session'
            }, status=404)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def start_recording(request, session_id):
    """Start recording the interview session."""
    try:
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        
        # Create or get existing recording
        recording, created = InterviewRecording.objects.get_or_create(
            session=session,
            defaults={'recording_started_at': timezone.now()}
        )
        
        if not created:
            # Update existing recording
            recording.recording_started_at = timezone.now()
            recording.recording_ended_at = None
            recording.duration_seconds = None
            recording.save()
        
        return JsonResponse({
            'success': True,
            'recording_id': recording.id,
            'message': 'Recording started successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def stop_recording(request, session_id):
    """Stop recording the interview session."""
    try:
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        
        try:
            recording = session.recording
            recording.recording_ended_at = timezone.now()
            
            # Calculate duration
            if recording.recording_started_at:
                duration = recording.recording_ended_at - recording.recording_started_at
                recording.duration_seconds = int(duration.total_seconds())
            
            recording.save()
            
            return JsonResponse({
                'success': True,
                'duration_seconds': recording.duration_seconds,
                'message': 'Recording stopped successfully'
            })
            
        except InterviewRecording.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'No recording found for this session'
            }, status=404)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def upload_video(request):
    """Upload video recording for an interview session."""
    try:
        session_id = request.POST.get('session_id')
        if not session_id:
            return JsonResponse({'error': 'Session ID required'}, status=400)
        
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        
        if 'video' not in request.FILES:
            return JsonResponse({'error': 'No video file provided'}, status=400)
        
        video_file = request.FILES['video']
        
        # Get or create recording object
        recording, created = InterviewRecording.objects.get_or_create(
            session=session,
            defaults={'recording_started_at': timezone.now()}
        )
        
        # Save the video file
        recording.video_file = video_file
        recording.save()
        
        return JsonResponse({
            'success': True,
            'video_url': recording.video_file.url,
            'message': 'Video uploaded successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
