from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(['GET'])
def get_messages(request):
    messages = ChatMessage.objects.order_by('-timestamp')[:50]
    data = [
        {
            "username": msg.username,
            "message": msg.message,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]
    return Response(data)


@api_view(['POST'])
def post_message(request):
    data = request.data
    msg = ChatMessage(username=data['username'], message=data['message'])
    msg.save()
    return Response({"status": "Message saved"})


@csrf_exempt
def ask_ai(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        question = body.get('question', '')
        # You can integrate OpenAI or your own logic here
        answer = f"You asked: {question}. Here is a mock reply."
        return JsonResponse({'answer': answer})


