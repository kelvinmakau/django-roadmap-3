from django.shortcuts import render, redirect
from .models import Message

# Create your views here.
def chat_view(request):
    messages = Message.objects.all()
    return render(request, 'chat/chat.html', {'messages': messages})

def send_message(request):
    if request.method == 'POST':
        user = request.POST['user']
        content = request.POST['content']
        Message.objects.create(user=user, content=content)

    return redirect('chat')
