from django import forms
from .models import Assignment, Submission, Feedback

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
def clean_password2(self):
        # Bypass password validation
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
# Login Form
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description','deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Use datetime picker
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['student_id','student_name', 'file', 'comments']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['teacher_name', 'comments','remarks']
class EmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)      