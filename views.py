from django.contrib import messages 
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, Submission, Feedback
from .forms import AssignmentForm, SubmissionForm, FeedbackForm
import os
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.shortcuts import render
from django.urls import reverse
import time
import cv2
import face_recognition
import numpy as nps
from django.conf import settings
from .forms import EmailForm


# Register View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to home page after registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, 'Invalid username or password.')
       
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout View


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to home page after logout

# Student view: Submit assignment
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment  # Link submission to the assignment
            submission.save()
            return redirect('home')
    else:
        form = SubmissionForm()
    messages.success(request, 'Your assignment has been submitted successfully!')
    return render(request, 'submit_assignment.html', {'form': form, 'assignment': assignment})

# Teacher view: View submissions for a specific assignment
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'view_submissions.html', {'submissions': submissions, 'assignment': assignment})
def viewst_submissi(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)

    # Handle search functionality
    student_id = request.GET.get('student_id')
    if student_id:
        submissions = submissions.filter(student_id__icontains=student_id)

    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'viewst_submissi.html', context)

# Teacher view: Leave feedback for a submission
def leave_feedback(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.submission = submission
            feedback.save()
            return redirect('staff')  # Redirect to a success page
    else:
        form = FeedbackForm()
    return render(request, 'leave_feedback.html', {'submission': submission, 'form': form})

# Admin view: Create assignments
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'create_assignment.html', {'form': form})

# List all assignments
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment_list.html', {'assignments': assignments})
def assignmentst_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignmentst_list.html', {'assignments': assignments})

def view_feedback(request, submission_id):
    # Fetch the submission or return a 404 error if not found
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Fetch the first feedback associated with the submission (if any)
    feedback = Feedback.objects.filter(submission=submission).first()
    
    # Render the template with the submission and feedback
    return render(request, 'view_feedback.html', {
        'submission': submission,
        'feedback': feedback
    })
def delete_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Delete the file from the filesystem
    if submission.file:
        file_path = os.path.join(settings.MEDIA_ROOT, submission.file.name)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Delete the submission from the database
    submission.delete()
    messages.success(request, 'Submission deleted successfully.')
    return redirect('assignment_list')
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Delete associated submissions and their files
    for submission in assignment.submission_set.all():
        if submission.file:
            file_path = os.path.join(settings.MEDIA_ROOT, submission.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)
    
    # Delete the assignment
    assignment.delete()
    
    # Add a success message
    messages.success(request, 'Assignment deleted successfully.')
    
    return redirect('assignment_list')

def staff(request):
    assignments = Assignment.objects.all()  # Fetch all assignments
    total_assignments = Assignment.objects.count()  # Total assignments
    total_submissions = Submission.objects.count()  # Total submissions
    completed_submissions = Submission.objects.filter().count()  # Completed submissions
    pending_feedback = Feedback.objects.filter().count()  # Pending feedback

    # Combine all data into a single context dictionary
    context = {
        'assignments': assignments,
           'assignment': assignments.first(),  # Add assignments to the context
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'completed_submissions': completed_submissions,
        'pending_feedback': pending_feedback,
    }
    return render(request, 'staff.html', context)

def assignment_detail(request, assignment_id):
 assignments = Assignment.objects.all()  # Fetch all assignments
      # Debugging: Check if assignments are fetched
 context = {
        'assignments': assignments,  # Pass assignments to the template
 }
 return render(request, 'assignment_detail.html', context)

def home(request):
    assignments = Assignment.objects.all()
    return render(request, 'home.html', {'assignments': assignments})
def assignment_de(request, assignment_id):
    # Fetch the assignment or return a 404 error if not found
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'assignment_de.html', {'assignment': assignment})

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = 'teja123@gmail.com'
            recipient_email = 'teja123@gmail.com'
            
            # Create the email message
            email_message = f"Feedback from {name} ({email}):\n\n{message}"
            
            send_mail(subject, email_message, from_email, [recipient_email])
            return HttpResponse('Feedback sent successfully!', status=200)
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})
KNOWN_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'kelly', 'teju.jpg')
known_image = face_recognition.load_image_file(KNOWN_IMAGE_PATH)
known_face_encoding = face_recognition.face_encodings(known_image)[0]


known_face_encodings = [known_face_encoding]
known_face_names = ["Authorized Person"]

def capture_frame(timeout=10):
    """
    Captures frames from the webcam for a specified duration.
    Returns the last captured frame or None if no frames are captured.
    """
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return None

    start_time = time.time()
    frames = []
    while time.time() - start_time < timeout:
        ret, frame = video_capture.read()
        if ret:
            frames.append(frame)
        time.sleep(0.1)  

    video_capture.release()

    if not frames:
        print("Error: No frames captured.")
        return None


    return frames[-1]

def detect_motion(prev_frame, curr_frame, threshold=5000):
    """
    Detects motion between two frames.
    Returns True if motion is detected, otherwise False.
    """
    diff = cv2.absdiff(prev_frame, curr_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > threshold:
            return True
    return False

def recognize_face(live_feed_duration=10, motion_threshold=5000):
    """
    Recognizes faces in the live feed and checks if it matches the known face.
    Only grants access if a live face with motion is detected.
    """
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    start_time = time.time()
    prev_frame = None

    while time.time() - start_time < live_feed_duration:
        ret, frame = video_capture.read()
        if not ret:
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)
        rgb_small_frame = small_frame[:, :, ::-1]

       
        if prev_frame is not None and detect_motion(prev_frame, small_frame, motion_threshold):

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                if True in matches:
                    video_capture.release()
                    return True

        prev_frame = small_frame

    video_capture.release()
    return False

def index(request):
    """
    Renders the home page.
    """
    return render(request, 'index.html')

def check_face(request):
    """
    Checks if the captured face matches the known face.
    Redirects to the success or failure page based on the result.
    """
    print("Checking face...")
    try:
        # Perform face recognition
        if recognize_face():
            print("Face recognized. Redirecting to success page.")
            return redirect(reverse('staff'))
        else:
            print("Face not recognized. Redirecting to failure page.")
            return redirect(reverse('failure'))
    except Exception as e:
        print(f"Error during face recognition: {e}")
        return redirect(reverse('failure'))


def failure(request):
    """
    Renders the failure page.
    """
    return render(request, 'failure.html')
def about(request):
    """
    Renders the failure page.
    """
    return render(request, 'about.html')