from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# Signal to create a Profile instance when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save the Profile instance when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50) # Student name instead of user
    file = models.FileField(upload_to='submissions/')
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.student_name} - {self.assignment.title}"

class Feedback(models.Model):
     REMARKS_CHOICES = [
        ('5', '5 - Excellent'),
        ('4', '4 - Very Good'),
        ('3', '3 - Good'),
        ('2', '2 - Average'),
        ('1', '1 - Poor'),
 ]
     submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='feedbacks')
     teacher_name = models.CharField(max_length=100)
     remarks = models.CharField(max_length=2, choices=REMARKS_CHOICES, default='5')
     comments = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f"Feedback by {self.teacher_name} for {self.submission.student_name}"