from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
from .models import InterviewSession, ChatMessage, CodeSubmission, Problem
from .ai_agent import AIInterviewAgent


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
        # Generate AI feedback
        ai_agent = AIInterviewAgent()
        feedback = ai_agent.generate_feedback(session)
        
        # Update session
        session.status = 'completed'
        session.completed_at = timezone.now()
        session.ai_feedback = feedback
        session.save()
        
        return redirect('interview_results', session_id=session.id)
    
    return render(request, 'ai_interview/complete_interview.html', {'session': session})


@login_required
def interview_results(request, session_id):
    """Display interview results and feedback."""
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    
    # Get all messages and code submissions
    messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    code_submissions = CodeSubmission.objects.filter(session=session).order_by('timestamp')
    
    context = {
        'session': session,
        'messages': messages,
        'code_submissions': code_submissions,
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
    
    # Extract test cases from problem examples
    test_cases = []
    if session.problem.examples:
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
