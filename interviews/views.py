from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Interview, InterviewNote, InterviewFeedbackPoint
from accounts.supabase_client import upload_file_to_storage, get_file_from_storage
import json


@login_required
def interview_list_view(request):
    """List all interviews for the current user"""
    interviews = Interview.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        interviews = interviews.filter(status=status_filter)
    
    context = {
        'interviews': interviews,
        'status_filter': status_filter,
    }
    
    return render(request, 'interviews/interview_list.html', context)


@login_required
def interview_detail_view(request, interview_id):
    """Display detailed view of a single interview"""
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    notes = interview.notes.all()
    feedback_points = interview.feedback_points.all()
    
    # Organize feedback by category
    feedback_by_category = {}
    for point in feedback_points:
        if point.category not in feedback_by_category:
            feedback_by_category[point.category] = {'strengths': [], 'improvements': []}
        
        if point.is_positive:
            feedback_by_category[point.category]['strengths'].append(point.point)
        else:
            feedback_by_category[point.category]['improvements'].append(point.point)
    
    context = {
        'interview': interview,
        'notes': notes,
        'feedback_by_category': feedback_by_category,
    }
    
    return render(request, 'interviews/interview_detail.html', context)


@login_required
def create_interview_view(request):
    """Create a new interview (placeholder for now, will be integrated with AI)"""
    if request.method == 'POST':
        # This is a simplified version - in production, this would be triggered by the AI system
        interview = Interview.objects.create(
            user=request.user,
            title=request.POST.get('title', 'Mock Interview'),
            problem_name=request.POST.get('problem_name', 'Sample Problem'),
            problem_description=request.POST.get('problem_description', ''),
            problem_difficulty=request.POST.get('difficulty', 'medium'),
            programming_language=request.POST.get('language', 'python'),
            status='scheduled'
        )
        
        messages.success(request, 'Interview scheduled successfully!')
        return redirect('interview_detail', interview_id=interview.id)
    
    return render(request, 'interviews/create_interview.html')


@login_required
def upload_recording_view(request, interview_id):
    """Upload interview recording to Supabase storage"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    
    if 'recording' not in request.FILES:
        return JsonResponse({'error': 'No recording file provided'}, status=400)
    
    recording_file = request.FILES['recording']
    
    try:
        # Generate unique file path
        file_path = f"interviews/{request.user.id}/{interview.id}/recording_{timezone.now().timestamp()}.webm"
        
        # Upload to Supabase storage
        result = upload_file_to_storage(
            bucket_name='interview-recordings',
            file_path=file_path,
            file_data=recording_file.read(),
            content_type=recording_file.content_type
        )
        
        if result.get('success'):
            # Update interview with recording info
            interview.recording_url = result['url']
            interview.recording_path = result['path']
            interview.save()
            
            return JsonResponse({
                'success': True,
                'url': result['url'],
                'message': 'Recording uploaded successfully'
            })
        else:
            return JsonResponse({
                'error': result.get('error', 'Upload failed')
            }, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def save_interview_data_view(request, interview_id):
    """
    Save interview data including code, transcript, and feedback
    This endpoint will be called by the AI interview system
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        
        # Update interview with submitted data
        if 'code' in data:
            interview.submitted_code = data['code']
        
        if 'transcript' in data:
            interview.transcript = data['transcript']
        
        if 'status' in data:
            interview.status = data['status']
            if data['status'] == 'in_progress' and not interview.started_at:
                interview.started_at = timezone.now()
            elif data['status'] == 'completed' and not interview.completed_at:
                interview.completed_at = timezone.now()
        
        # Save scores
        if 'scores' in data:
            scores = data['scores']
            interview.overall_score = scores.get('overall')
            interview.communication_score = scores.get('communication')
            interview.problem_solving_score = scores.get('problem_solving')
            interview.code_quality_score = scores.get('code_quality')
        
        # Save feedback
        if 'feedback_report' in data:
            interview.feedback_report = data['feedback_report']
        
        if 'strengths' in data:
            interview.strengths = data['strengths']
        
        if 'areas_for_improvement' in data:
            interview.areas_for_improvement = data['areas_for_improvement']
        
        interview.save()
        
        # Save individual feedback points if provided
        if 'feedback_points' in data:
            for point_data in data['feedback_points']:
                InterviewFeedbackPoint.objects.create(
                    interview=interview,
                    category=point_data['category'],
                    is_positive=point_data['is_positive'],
                    point=point_data['point']
                )
        
        # Save notes if provided
        if 'notes' in data:
            for note_data in data['notes']:
                InterviewNote.objects.create(
                    interview=interview,
                    content=note_data['content'],
                    note_type=note_data.get('type', 'observation'),
                    timestamp=note_data.get('timestamp', timezone.now())
                )
        
        return JsonResponse({
            'success': True,
            'message': 'Interview data saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def delete_interview_view(request, interview_id):
    """Delete an interview"""
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    
    if request.method == 'POST':
        interview.delete()
        messages.success(request, 'Interview deleted successfully!')
        return redirect('interview_list')
    
    return render(request, 'interviews/confirm_delete.html', {'interview': interview})
