from  rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
#here i am hashing the password
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user    


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate(Self, data):
        if 'age' in data and data['age'] < 18:
            raise serializers.ValidationError({'error':"age cannot be less than 18"})  
        
        if 'name' in data and data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({'error':"name should not contain digit"})  

        if 'father_name' in data and data['father_name']:
            for n in data['father_name']:
                if n.isdigit():
                    raise serializers.ValidationError({'error':"father name should not contain digit"})  

        return data  


class CategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerialiser(serializers.ModelSerializer):
    category = CategorySerialiser()
    class Meta:
        model = Book
        fields = '__all__'
                