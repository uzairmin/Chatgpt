from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.serializers import UsersSerializer
from rest_framework.generics import ListAPIView
from authentication.models import User
from rest_framework import status
from settings.helpers import custom_validation, own_user_check

class UserRegistration(APIView):

  def create_user(self, email, password, full_name):
    if not custom_validation('email', email):
      return status.HTTP_400_BAD_REQUEST, "This is not an email address"
    user_exist = User.objects.filter(email=email)
    if user_exist.exists():
      return status.HTTP_400_BAD_REQUEST, "User already exists with this email address"
    if not custom_validation('full_name', full_name):
      return status.HTTP_400_BAD_REQUEST, "First name starts with a capital letter and no special characters are allowed"
    if not custom_validation('password', password):
      return status.HTTP_400_BAD_REQUEST, "Password must contains at least eight characters, including at least one number and includes both lower and uppercase letters and special characters"


    user = User.objects.create(email=email, full_name=full_name)
    user.set_password(password)
    user.save()
    return status.HTTP_201_CREATED, "User created successfully"

  def get(self, request, pk):
    try:
      user = User.objects.get(pk=pk)
      serializer = UsersSerializer(user, many=False)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except:
      return Response("No such user exists with this id", status=status.HTTP_400_BAD_REQUEST)

  def post(self, request):
    email = request.data.get('email')
    password = request.data.get('password')
    full_name = request.data.get('full_name')

    condition_1 = [
      email != "",
      password != "",
      full_name != "",
    ]

    condition_2 = [
      email != None,
      password != None,
      full_name != None,
    ]

    if all(condition_1):
      if all(condition_2):
        http_status, msg = self.create_user(email, password, full_name)
        return Response(msg, status=http_status)
      else:
        return Response("Field/s is/are missing", status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response("Required fields can't be empty", status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk):
    try:
      if own_user_check(request, pk):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        full_name = request.data.get('full_name', '')
        user = User.objects.get(pk=pk)
        if email != '':
          user_exist = User.objects.filter(email=email)
          if user_exist.exists():
            if user_exist.first().id == pk:
              return Response("This user already exist with this email", status=status.HTTP_400_BAD_REQUEST)
            return Response("User with this email already exists", status=status.HTTP_400_BAD_REQUEST)
          user.email = email
        if password != '':
          user.set_password(password)
        if full_name != '':
          user.full_name = full_name
        user.save()
        user = User.objects.get(pk=pk)
        query = UsersSerializer(user)
        return Response(query.data, status=status.HTTP_200_OK)
      else:
        return Response("You are unauthorized", status=status.HTTP_400_BAD_REQUEST)
    except:
      return Response("No user with found with this id", status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    try:
      if own_user_check(request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response("User deleted succesfully", status=status.HTTP_200_OK)
      else:
        return Response("You are unauthorized", status=status.HTTP_400_BAD_REQUEST)
    except:
      return Response("No user with found with this id", status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(ListAPIView):

  def get(self, request):
    user = User.objects.all()
    serializer = UsersSerializer(user, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

