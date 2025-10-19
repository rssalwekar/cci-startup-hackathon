from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import InterviewReport
from .report_generator import ReportGenerator
from ai_interview.models import InterviewSession  # Adjust to your session model location


@csrf_exempt
@require_http_methods(["POST"])
def generate_report(request):
    """
    Generate report using Kronos Labs

    POST /api/report/generate/
    Body: {"session_id": 123}
    """
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')

        if not session_id:
            return JsonResponse({
                'success': False,
                'error': 'session_id required'
            }, status=400)

        # Check if report exists
        existing = InterviewReport.objects.filter(session_id=session_id).first()
        if existing:
            return JsonResponse({
                'success': True,
                'report_id': existing.id,
                'message': 'Report already exists'
            })

        # Fetch interview/session data directly from Django models
        try:
            interview = InterviewSession.objects.get(id=session_id)
        except InterviewSession.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Interview not found'
            }, status=404)

        # Prepare interview data as dict (adjust field names as needed)
        interview_data = {
            'problem_title': getattr(interview, 'problem_title', ''),
            'difficulty': getattr(interview, 'difficulty', ''),
            'time_taken': getattr(interview, 'time_taken', 0),
            'test_cases_passed': getattr(interview, 'test_cases_passed', 0),
            'total_test_cases': getattr(interview, 'total_test_cases', 0),
            'programming_language': getattr(interview, 'programming_language', 'python'),
            'code_submission': getattr(interview, 'code_submission', ''),
            'chat_transcript': getattr(interview, 'chat_transcript', ''),
        }

        # Generate report with Kronos
        generator = ReportGenerator()
        report_data = generator.analyze_interview(interview_data)

        # Save to database
        report = InterviewReport.objects.create(
            session_id=session_id,
            overall_score=report_data['overall_score'],
            code_quality_score=report_data['code_quality_score'],
            communication_score=report_data['communication_score'],
            problem_solving_score=report_data['problem_solving_score'],
            time_management_score=report_data['time_management_score'],
            code_analysis=report_data['code_analysis'],
            communication_analysis=report_data['communication_analysis'],
            strengths=report_data['strengths'],
            weaknesses=report_data['weaknesses'],
            improvement_tips=report_data['improvement_tips'],
            recommended_resources=report_data['recommended_resources'],
            detailed_feedback=report_data['detailed_feedback']
        )

        return JsonResponse({
            'success': True,
            'report_id': report.id,
            'session_id': session_id,
            'scores': {
                'overall': report.overall_score,
                'code_quality': report.code_quality_score,
                'communication': report.communication_score,
                'problem_solving': report.problem_solving_score,
                'time_management': report.time_management_score
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_report(request, report_id):
    """Get report by ID"""
    try:
        report = InterviewReport.objects.get(id=report_id)

        return JsonResponse({
            'success': True,
            'report': {
                'id': report.id,
                'session_id': report.session_id,
                'overall_score': report.overall_score,
                'code_quality_score': report.code_quality_score,
                'communication_score': report.communication_score,
                'problem_solving_score': report.problem_solving_score,
                'time_management_score': report.time_management_score,
                'code_analysis': report.code_analysis,
                'communication_analysis': report.communication_analysis,
                'strengths': report.strengths,
                'weaknesses': report.weaknesses,
                'improvement_tips': report.improvement_tips,
                'recommended_resources': report.recommended_resources,
                'detailed_feedback': report.detailed_feedback,
                'created_at': report.created_at.isoformat()
            }
        })

    except InterviewReport.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)


@require_http_methods(["GET"])
def view_report_by_session(request, session_id):
    """Get report by session ID"""
    try:
        report = InterviewReport.objects.get(session_id=session_id)

        return JsonResponse({
            'success': True,
            'report': {
                'id': report.id,
                'session_id': report.session_id,
                'overall_score': report.overall_score,
                'created_at': report.created_at.isoformat()
            }
        })

    except InterviewReport.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)
