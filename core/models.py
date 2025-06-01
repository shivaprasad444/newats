from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=[
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced")
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
    

class Timesheets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_period_start = models.DateField(default=date.today)
    pay_period_end = models.DateField(default=date.today)
    date = models.DateField()
    earn_code = models.CharField(
    max_length=100,
    choices=[
        ('Regular Pay', 'Regular Pay'),
        ('Overtime', 'Overtime'),
    ],
    default='Regular Pay'  
)
    start_time = models.TimeField()
    end_time = models.TimeField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date}"