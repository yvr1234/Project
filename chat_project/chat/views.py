from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat  # Assuming you have a Chat model to store messages
from django.http import JsonResponse

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('chat')  # Redirect to chat page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()

    return render(request, 'chat/signup.html', {'form': form})


# Chat view - only accessible if user is authenticated
@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user
    return render(request, 'chat/chat.html', {'users': users})


# Chat window view to display messages between two users
@login_required
def chat_window(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    
    # Fetch messages between the logged-in user and the selected user
    messages = Chat.objects.filter(sender=request.user, receiver=receiver) | Chat.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')  # Sort messages by timestamp
    
    # Handle sending messages
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Chat.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('chat_window', user_id=user_id)
    
    return render(request, 'chat/chat_window.html', {'messages': messages, 'receiver': receiver})


# API to fetch old messages (for the "Load Old Messages" button)
@login_required
def load_old_messages(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    
    # Fetch old messages in reverse order
    messages = Chat.objects.filter(sender=request.user, receiver=receiver) | Chat.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('-timestamp')[:10]  # Load last 10 messages for now
    
    # Convert messages to JSON format
    messages_data = [
        {
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in messages
    ]
    
    return JsonResponse({'messages': messages_data})