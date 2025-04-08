from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from userauths.models import Profile, User
from django.contrib.auth.password_validation import validate_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True, required =True, validators =[validate_password])
    password2 = serializers.CharField(write_only =True, required =True)

    class Meta:
        model = User
        fields = ['full_name','email','password','password2']

    def validate(self,attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({'password': 'Password mismatch'})

        return attr

    def create(self, validate_data):
        user = User.objects.create(
            full_name = validate_data['full_name'],
            email = validate_data['email'],
        )

        email_username, _ = user.email.split("@")
        user.username = email_username
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'