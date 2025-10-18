from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_interview, name='start_interview'),
    path('interview/<int:session_id>/', views.interview_page, name='interview_page'),
    path('complete/<int:session_id>/', views.complete_interview, name='complete_interview'),
    path('results/<int:session_id>/', views.interview_results, name='interview_results'),
    path('api/submit-code/<int:session_id>/', views.submit_code, name='submit_code'),
    path('api/session-data/<int:session_id>/', views.get_session_data, name='get_session_data'),
]

