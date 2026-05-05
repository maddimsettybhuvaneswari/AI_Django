from rest_framework import serializers
from .models import User, Doctor
from .models import Appointment
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"