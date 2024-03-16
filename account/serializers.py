from  rest_framework import serializers
from .models import *
from .helpers import *
from django.contrib.auth.models import User

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password']
#here i am hashing the password
    def create(self, validated_data):
        user = CustomUser.objects.create(email = validated_data['email'], phone = validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        send_otp_to_mobile(user.phone, user)
        return user    
