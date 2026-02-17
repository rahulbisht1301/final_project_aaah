from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import User, Message


@login_required
def role_based_redirect(request):
    if request.user.role == 'INVESTOR':
        return redirect('investor_dashboard')
    elif request.user.role == 'STARTUP':
        return redirect('startup_dashboard')
    elif request.user.role == 'MANUFACTURER':
        return redirect('manufacturer_dashboard')
    elif request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {
                'error': 'Username already exists'
            })
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        
        login(request, user)
        return redirect('role_redirect')
    
    return render(request, 'registration/register.html')


@login_required
def inbox(request):
    """View inbox messages."""
    received = Message.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = received.filter(is_read=False).count()
    
    return render(request, 'accounts/inbox.html', {
        'messages_list': received,
        'unread_count': unread_count,
    })


@login_required
def sent_messages(request):
    """View sent messages."""
    sent = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    return render(request, 'accounts/sent.html', {
        'messages_list': sent,
    })


@login_required
def view_message(request, message_id):
    """View a single message."""
    msg = get_object_or_404(Message, id=message_id)
    
    # Only sender or recipient can view
    if msg.sender != request.user and msg.recipient != request.user:
        return redirect('inbox')
    
    # Mark as read if recipient
    if msg.recipient == request.user and not msg.is_read:
        msg.is_read = True
        msg.save()
    
    return render(request, 'accounts/message_detail.html', {'msg': msg})


@login_required
def compose_message(request, recipient_id=None):
    """Compose a new message."""
    recipient = None
    if recipient_id:
        recipient = get_object_or_404(User, id=recipient_id)
    
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        
        recipient = get_object_or_404(User, id=recipient_id)
        
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            content=content
        )
        
        messages.success(request, f'Message sent to {recipient.username}!')
        return redirect('sent_messages')
    
    # Get list of users to message (exclude self)
    users = User.objects.exclude(id=request.user.id).order_by('username')
    
    return render(request, 'accounts/compose.html', {
        'recipient': recipient,
        'users': users,
    })
