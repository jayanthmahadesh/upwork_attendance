from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# StaffMember model
class StaffMember(models.Model):
    # Linking each staff member to Django's built-in User model for authentication and extending it
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

# Roster model


class Roster(models.Model):
    staff_member = models.ForeignKey(StaffMember, on_delete=models.CASCADE)
    # Example: "Monday, Wednesday, Friday"
    working_days = models.CharField(max_length=255)
    SHIFT_CHOICES = (
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Night', 'Night'),
    )
    shifts = models.CharField(max_length=10, choices=SHIFT_CHOICES)

    def __str__(self):
        return f"{self.staff_member.name}'s Roster"

# AttendanceRecord model


class AttendanceRecord(models.Model):
    staff_member = models.ForeignKey(StaffMember, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    # Assuming media is configured
    image = models.ImageField(upload_to='attendance_images/')

    def __str__(self):
        return f"Attendance for {self.staff_member.name} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
