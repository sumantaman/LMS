from django.shortcuts import render
from api import serailizer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
import random
from django.conf import settings
from rest_framework.permissions import AllowAny
from userauths.models import *
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# from api import serializer as api_serializer
# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classas = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer

def generate_random_otp(lenght=7):
    opt =''.join([str(random.randint(0,9)) for _ in range(lenght)])
    return opt

class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class =api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user = User.objects.filter(email=email).first()

        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            user.refresh_token = refresh_token
            user.otp =generate_random_otp()
            user.save()

            link = f"https://localhost:5173/create-new-password/?otp{user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}"
            merge_data = {
                "link":link,
                "username":user.username
            }
            subject ="password reset email"
            text_body=render_to_string("email/password_reset.txt",merge_data)
            html_body=render_to_string("email/password_reset.html",merge_data)

            msg = EmailMultiAlternatives(subject=subject,
            from_email=settings.FROM_EMAIL,
            to=[user.email],
            body=text_body,
            )
            print("link ===",link)
            msg.attach_alternative(html_body,"text/html")
            msg.send()
        return user

# changing password
class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer
# difference of args, kwargs
    def create(self, request,*args,**kwargs):
        opt = request.data['opt']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']


        user = User.objects.get(id=uuidb64, otp= otp)

        if user:
            user.set_password(password)
            user.otp =""
            user.save()
            return Response({"message": "password changed"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "invalid otp"}, status=status.HTTP_400_BAD_REQUEST)