from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('assignment_list', views.assignment_list, name='assignment_list'),
    path('assignment/create/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('assignment/<int:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),
    path('submission/<int:submission_id>/feedback/', views.leave_feedback, name='leave_feedback'),
     path('submission/<int:submission_id>/delete/', views.delete_submission, name='delete_submission'), 
]