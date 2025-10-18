from django.urls import path
from . import views

urlpatterns = [
    path('', views.interview_list_view, name='interview_list'),
    path('<int:interview_id>/', views.interview_detail_view, name='interview_detail'),
    path('create/', views.create_interview_view, name='create_interview'),
    path('<int:interview_id>/upload-recording/', views.upload_recording_view, name='upload_recording'),
    path('<int:interview_id>/save-data/', views.save_interview_data_view, name='save_interview_data'),
    path('<int:interview_id>/delete/', views.delete_interview_view, name='delete_interview'),
]
