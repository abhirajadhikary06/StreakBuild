from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UploadImageForm, FieldOfInterestForm
from .models import Profile, Challenge, UploadedImage, Badge
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, FieldOfInterestForm, UploadImageForm
from .models import Profile, Challenge, UploadedImage, Badge, Notification
from .utils import suggest_challenges  # Import the function

import requests

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('imageboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'tracker/login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, "Account created successfully!")
            return redirect('imageboard')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})



def suggest_challenges(fields_of_interest):
    # Use predefined relationships from the database as a fallback
    suggested_challenges = []
    for field in fields_of_interest:
        suggested_challenges.extend(field.challenges.all())
    return list(set(suggested_challenges))[:15]  # Return up to 15 unique challenges


@login_required
def dashboard(request):
    # Get suggested challenges from the session (or database)
    suggested_challenge_ids = request.session.get('suggested_challenges', [])
    suggested_challenges = Challenge.objects.filter(id__in=suggested_challenge_ids)
    
    # Get all uploaded images for the suggested challenges
    uploads = UploadedImage.objects.filter(user=request.user)
    
    # Calculate progress for each challenge
    progress = {}
    for challenge in suggested_challenges:
        count = uploads.filter(challenge=challenge).count()
        progress[challenge.name] = (count / challenge.total_days) * 100 if challenge.total_days > 0 else 0
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    return render(request, 'tracker/imageboard.html', {
        'challenges': suggested_challenges,
        'progress': progress,
        'uploads': uploads,
        'unread_notifications': unread_notifications
    })


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id, user=request.user)
    challenge = image.challenge
    image.delete()
    messages.success(request, "Image deleted successfully.")
    
    # Check if the badge needs to be revoked
    uploads_count = UploadedImage.objects.filter(user=request.user, challenge=challenge).count()
    if uploads_count < challenge.total_days:
        Badge.objects.filter(user=request.user, challenge=challenge).delete()
    
    return redirect('imageboard')

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            challenge = form.cleaned_data['challenge']
            
            # Check if the user has already completed the challenge
            uploads_count = UploadedImage.objects.filter(user=request.user, challenge=challenge).count()
            if uploads_count >= challenge.total_days:
                messages.warning(request, f"You have already completed the '{challenge.name}' challenge.")
                return redirect('imageboard')
            
            # Save the uploaded image
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            
            # Check if the user has now completed the challenge
            uploads_count += 1
            if uploads_count >= challenge.total_days:
                Badge.objects.get_or_create(user=request.user, challenge=challenge)
                Notification.objects.create(
                    user=request.user,
                    message=f"You have completed the '{challenge.name}' challenge!"
                )
                messages.success(request, f"Congratulations! You've earned the '{challenge.name}' badge!")
            
            return redirect('imageboard')
    else:
        form = UploadImageForm()
    return render(request, 'tracker/upload_image.html', {'form': form})

@login_required
def mark_notifications_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('imageboard')

@login_required
def profile(request):
    profile = request.user.profile
    badges = Badge.objects.filter(user=request.user)
    challenges = Challenge.objects.all()
    uploads = UploadedImage.objects.filter(user=request.user)
    progress = {}
    for challenge in challenges:
        count = uploads.filter(challenge=challenge).count()
        progress[challenge.name] = (count / challenge.total_days) * 100 if challenge.total_days > 0 else 0
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    return render(request, 'tracker/profile.html', {
        'profile': profile,
        'badges': badges,
        'progress': progress,
        'unread_notifications': unread_notifications
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')