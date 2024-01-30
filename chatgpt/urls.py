from django.urls import path
from chatgpt.views import ChatView

urlpatterns = [
  path('chat/', ChatView.as_view(), name='chat'),
]
