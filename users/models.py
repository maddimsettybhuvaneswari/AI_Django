from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobilenumber = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.user.username
    class Meta:
        db_table = 'profile'


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mobileNumber = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    profession = models.CharField(max_length=100)
    hospitalName = models.CharField(max_length=100)
    hospital_location = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
  
    class Meta:
        db_table = 'doctors'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default="pending")
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "appointment" 

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name}"


class Conversation(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Conversation {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.CharField(max_length=10)  # 'user' or 'ai'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     mobilenumber = models.CharField(max_length=15)

#     class Meta:
#         db_table = 'djangodoctusers'