from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class Login(APIView):

  def get(self, request):
    try:
      email = request.data.get('email')
      password = request.data.get('password')
      user = authenticate(email=email, password=password)
      if not user:
        return Response("Invalid email or password", status=status.HTTP_404_NOT_FOUND)
      if not user.is_active:
        return Response("User is no longer active, Contact Admin", status=status.HTTP_401_UNAUTHORIZED)
      refresh = RefreshToken.for_user(user)
      access = refresh.access_token
      login(request, user)
      return Response({"detail": "Logged in successfully", "refresh": str(refresh), "access": str(access)}, status=status.HTTP_200_OK)
    except:
      return Response("User with this email address does not exist", status=status.HTTP_404_NOT_FOUND)

class Logout(APIView):

  def get(self, request):
    logout(request)
    return Response("Logged out successfully", status=status.HTTP_200_OK)