from django.db import models
from settings.helpers import TimeStamped
from authentication.models import User

class Chatgpt(TimeStamped):
    chatgpt_input = models.TextField()
    chatgpt_response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
