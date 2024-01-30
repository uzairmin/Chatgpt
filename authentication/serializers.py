from rest_framework import serializers
from authentication.models import User

class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'full_name', 'email' ]
