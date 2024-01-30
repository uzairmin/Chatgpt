import openai
from django.conf import settings
from chatgpt.models import Chatgpt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ChatView(APIView):
    def post(self, request):
        try:
            input = request.data.get('input', '')
            if not input:
                return Response('User input is required', status=status.HTTP_400_BAD_REQUEST)
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.Completion.create(engine="gpt-3.5-turbo-0613", prompt=input, max_tokens=150)
            reply = response['choices'][0]['text'].strip()
            Chatgpt.objects.create(chatgpt_input=input, chatgpt_response=reply, user=request.user)
            return Response(reply, status=status.HTTP_201_CREATED)
        except:
            return Response("Something went wrong with Chatgpt", status=status.HTTP_400_BAD_REQUEST)
        