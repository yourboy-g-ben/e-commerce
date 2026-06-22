from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from authenticate.serializers import SignUpSerializer, LoginSerializer
from authenticate.models import User
from django.contrib import auth
# Create your views here.

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer._validated_data.get("email")
        password = serializer._validated_data.get("password")
        email_exists = User.objects.filter(email=email).first()
        if email_exists:
           return Response(data={"message": "Account with this email already exists"}, status = 400)
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(data={"message": "Account created successfully"}, status=201)


class LoginVew(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email").lower()
        password = serializer.validated_data.get("password")
        # user = User.objects.filter(email=email).first()
        user = auth.authenticate(email=email, password=password)
        if not user:
            return Response(data={"message": "Invalid credentials"}, status=400)
        return Response(data=user.get_tokens(), status=200)
    


