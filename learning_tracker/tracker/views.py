from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UploadFileForm, FieldOfInterestForm
from .models import Profile, Challenge, Badge, UploadedFile, Notification
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import suggest_challenges  # Import the function
import os
import requests

def landing_page(request):
    print("Landing page view accessed")
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/landing_page.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
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
            return redirect('dashboard')
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
    
    # Get all uploaded files for the suggested challenges
    uploads = UploadedFile.objects.filter(user=request.user)
    
    # Calculate progress for each challenge
    progress = {}
    for challenge in suggested_challenges:
        count = uploads.filter(challenge=challenge).count()
        progress[challenge.name] = (count / challenge.total_days) * 100 if challenge.total_days > 0 else 0
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    return render(request, 'tracker/dashboard.html', {
        'challenges': suggested_challenges,
        'progress': progress,
        'uploads': uploads,
        'unread_notifications': unread_notifications
    })

@login_required
def delete_file(request, file_id):
    file_instance = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    challenge = file_instance.challenge
    file_instance.delete()
    messages.success(request, "File deleted successfully.")
    
    # Check if the badge needs to be revoked
    uploads_count = UploadedFile.objects.filter(user=request.user, challenge=challenge).count()
    if uploads_count < challenge.total_days:
        Badge.objects.filter(user=request.user, challenge=challenge).delete()
    
    return redirect('dashboard')

import logging

logger = logging.getLogger(__name__)

@login_required
def upload_file(request):
    logger.info("Upload file view accessed")
    # Define the allowed file formats
    file_formats = [
        ".py", ".ipynb", ".csv", ".json", ".pkl", ".h5", ".onnx", ".tflite",
        ".js", ".html", ".css", ".ts", ".cpp", ".h", ".java", ".cs", ".rs", ".go", ".kt", ".swift",
        ".jsx", ".vue", ".svelte", ".graphql", ".yaml", ".yml", ".tf", ".sh", ".dockerfile",
        ".sol", ".pem", ".pcap", ".sql", ".bson", ".db", ".dart", ".tsx", ".md", ".uml",
        ".blueprint", ".fbx", ".obj", ".fig", ".xd", ".ai", ".psd", ".gitignore", ".ino"
    ]

    if request.method == 'POST':
        logger.info("Handling POST request")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("Form is valid")
            challenge = form.cleaned_data['challenge']
            uploaded_file = request.FILES['file']

            # Check if the file format is allowed
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            logger.info(f"Uploaded file extension: {file_extension}")
            if file_extension not in file_formats:
                logger.warning(f"Invalid file format: {file_extension}")
                return JsonResponse({
                    'status': 'error',
                    'message': f"Incorrect file format. Allowed formats: {', '.join(file_formats)}"
                })

            # Check if the user has already completed the challenge
            uploads_count = UploadedFile.objects.filter(user=request.user, challenge=challenge).count()
            if uploads_count >= challenge.total_days:
                logger.warning(f"User has already completed the challenge: {challenge.name}")
                return JsonResponse({
                    'status': 'error',
                    'message': f"You have already completed the '{challenge.name}' challenge."
                })

            # Save the uploaded file
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            logger.info("File saved successfully")

            # Check if the user has now completed the challenge
            uploads_count += 1
            if uploads_count >= challenge.total_days:
                Badge.objects.get_or_create(user=request.user, challenge=challenge)
                Notification.objects.create(
                    user=request.user,
                    message=f"You have completed the '{challenge.name}' challenge!"
                )
                logger.info("Badge and notification created")

            return JsonResponse({'status': 'success', 'message': 'File uploaded successfully.'})
        else:
            logger.error("Form is invalid")
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    else:
        logger.info("Handling GET request")
        form = UploadFileForm()
        return render(request, 'tracker/upload_file.html', {'form': form})

@login_required
def field_of_interest(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = FieldOfInterestForm(request.POST)
        if form.is_valid():
            profile.fields_of_interest.set(form.cleaned_data['fields_of_interest'])
            
            # Call the suggest_challenges function
            suggested_challenges = suggest_challenges(profile.fields_of_interest.all())
            
            # Store suggested challenges in the session (optional)
            request.session['suggested_challenges'] = [challenge.id for challenge in suggested_challenges]
            
            profile.save()
            return redirect('dashboard')
    else:
        form = FieldOfInterestForm()
    return render(request, 'tracker/field_of_interest.html', {'form': form})
    
@login_required
def mark_notifications_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('dashboard')

@login_required
def profile(request):
    profile = request.user.profile
    badges = Badge.objects.filter(user=request.user)
    challenges = Challenge.objects.all()
    uploads = UploadedFile.objects.filter(user=request.user)
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