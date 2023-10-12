from rest_framework import serializers
from restaurant_review.models import Client,Therapist,Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'