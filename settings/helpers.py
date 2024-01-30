import re
from django.db import models

# Validate strong password
def custom_validation(type, field):
  if type == 'password':
    pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
  elif type == 'email':
    pattern = r"^\S+@\S+\.\S+$"
  elif type == 'full_name':
    pattern = "^[a-zA-Z]{2,}(?: [a-zA-Z]+){0,2}$"
  return re.match(pattern, field) # Returns Match object

def own_user_check(request, pk):
  if request.user.id == pk:
    return True
  return False


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
