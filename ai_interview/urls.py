from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_interview, name='start_interview'),
    path('interview/<int:session_id>/', views.interview_page, name='interview_page'),
    path('complete/<int:session_id>/', views.complete_interview, name='complete_interview'),
    path('results/<int:session_id>/', views.interview_results, name='interview_results'),
    path('api/submit-code/<int:session_id>/', views.submit_code, name='submit_code'),
    path('api/session-data/<int:session_id>/', views.get_session_data, name='get_session_data'),
    path('get-test-cases/<int:session_id>/', views.get_test_cases, name='get_test_cases'),
    path('get-function-signature/<int:session_id>/', views.get_function_signature, name='get_function_signature'),
    path('api/synthesize-speech/', views.synthesize_speech, name='synthesize_speech'),
    path('api/available-voices/', views.get_available_voices, name='get_available_voices'),
    path('api/last-ai-message/<int:session_id>/', views.get_last_ai_message, name='get_last_ai_message'),
    path('api/start-recording/<int:session_id>/', views.start_recording, name='start_recording'),
    path('api/stop-recording/<int:session_id>/', views.stop_recording, name='stop_recording'),
    path('api/upload-video/', views.upload_video, name='upload_video'),
]

