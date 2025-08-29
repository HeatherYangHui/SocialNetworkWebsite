from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
from django.utils.timezone import localtime
import json


def home_view(request):
    if request.user.is_authenticated:
        return redirect('global_stream')  # Redirect to Global Stream if logged in
    return redirect('login')  # Redirect to Login if not logged in




@login_required
def global_stream_action(request):
    """View to display all posts and allow users to create new posts."""
    if request.method == "GET":
        posts = Post.objects.all().order_by('-creation_time') 
        return render(request, 'socialnetwork/global_stream.html', {'posts': Post.objects.all().order_by('-creation_time')})
    
    
    if 'post_text' not in request.POST or not request.POST['post_text'].strip():
        posts = Post.objects.all().order_by('-creation_time')
        return render(request, 'socialnetwork/global_stream.html', {
            'posts': Post.objects.all().order_by('-creation_time'),
            'error': "Post text cannot be empty."
        })
    
    new_post = Post.objects.create(text=request.POST['post_text'], user = request.user, creation_time = timezone.now())
    new_post.save()
    
    # return redirect('global_stream')
    return render(request, 'socialnetwork/global_stream.html', {'posts': Post.objects.all().order_by('-creation_time')})


@login_required
def follower_stream_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    """View to display posts from followed users in reverse-chronological order."""
    following_users = request.user.profile.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by('-creation_time')
    return render(request, 'socialnetwork/follower_stream.html', {'posts': posts})

@login_required
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_user = request.user

    if request.method == 'GET':
        context = {
            'form': ProfileForm(instance=profile),  #
            'profile': profile,
            'profile_user': profile_user,
            'following_users': profile.following.all()
        }
        return render(request, 'socialnetwork/my_profile.html', context)

    form = ProfileForm(request.POST, request.FILES, instance=profile)  # Correctly attach the profile instance

    if not form.is_valid():
        context = {'form': form, 'profile': profile, 'profile_user': profile_user}
        return render(request, 'socialnetwork/my_profile.html', context)

    form.save()  # Save the updated bio and picture
    
    profile.refresh_from_db()

    context = {
        'form': ProfileForm(instance=profile),  # Ensure updated data is loaded
        'profile': profile,
        'profile_user': profile_user
    }
    return render(request, 'socialnetwork/my_profile.html', context)

    
@login_required
def other_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    profile, created = Profile.objects.get_or_create(user=user)
    
    return render(request, 'socialnetwork/other_profile.html', {'profile': user.profile, 'profile_user': user})




@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # ensure using has a profile before adding to the list
    # added
    user_to_follow.profile, _ = Profile.objects.get_or_create(user=user_to_follow)
    request.user.profile, _ = Profile.objects.get_or_create(user=request.user)
    
    request.user.profile.following.add(user_to_follow)
    
    request.user.profile.save()
    
    profile = user_to_follow.profile
    return render(request,'socialnetwork/other_profile.html', {'profile':profile, 'profile_user': user_to_follow})

@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    
    profile = user_to_unfollow.profile
    return render(request,'socialnetwork/other_profile.html', {'profile':profile, 'profile_user': user_to_unfollow})


# Views for Authentication
def login_action(request):
    context = {
        'header_link': 'Register',
        'header_link_id': 'id_register_link',
        'header_link_url': 'register'
    }

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    form = LoginForm(request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'socialnetwork/login.html', context)

    # Authenticate user
    new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    
    if new_user is None:  # Handle case where authentication fails
        context['form'] = form
        context['error'] = "Invalid username or password"
        return render(request, 'socialnetwork/login.html', context)

    # Login and redirect
    login(request, new_user)
    return redirect('global_stream')



def logout_action(request):
    logout(request)
    return redirect('login')


def register_action(request):
    context = {'header_link': 'Login', 'header_link_id': 'id_login_link', 'header_link_url': 'login'}

    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    form = RegisterForm(request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'socialnetwork/register.html', context)

    # Check if the username already exists
    if User.objects.filter(username=form.cleaned_data['username']).exists():
        form.add_error('username', 'Username already taken. Please choose another one.')
        context['form'] = form
        return render(request, 'socialnetwork/register.html', context)

    # Create and save the new user
    new_user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name']
    )

    login(request, new_user)
    return redirect('global_stream')


@login_required
def photo(request, user_id):
    """Serves the profile picture of a user."""
    user = get_object_or_404(User, id=user_id)

    try:
        if not user.profile.picture:
            raise ObjectDoesNotExist  # If no picture exists, trigger 404 handling

        # Open and serve the profile image
        with open(user.profile.picture.path, "rb") as img:
            return HttpResponse(img.read(), content_type="image/jpeg")  
    except (ObjectDoesNotExist, FileNotFoundError):
        # Serve default image if no profile picture exists
        with open("static/socialnetwork/sample_profile.jpg", "rb") as default_img:
            return HttpResponse(default_img.read(), content_type="image/jpeg")

# Newly added for HW6


def get_global(request):
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    posts = Post.objects.all().order_by("-creation_time")  # Newest first
    post_list = []

    for post in posts:
        post_list.append({
            "id": post.id,
            "text": post.text,
            "user_id": post.user.id,
            "user_fullname": f"{post.user.first_name} {post.user.last_name}",
            "creation_time": post.creation_time.isoformat(),
            "comments": [
                {
                    "id": comment.id,
                    "text": comment.text,
                    "user_id": comment.user.id,
                    "user_fullname": f"{comment.user.first_name} {comment.user.last_name}",
                    "creation_time": comment.creation_time.isoformat()
                }
                for comment in post.comments.all().order_by("creation_time") # Oldest first
            ]
        })

    return JsonResponse({"posts": post_list}, safe=False)


@login_required
def get_follower(request):
    """Returns posts from followed users in JSON format."""
    following_users = request.user.profile.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by('creation_time')

    data = []
    for post in posts:
        comments = [
            {
                "id": comment.id,
                "text": comment.text,
                "user_id": comment.user.id,
                "user_fullname": f"{comment.user.first_name} {comment.user.last_name}",
                "creation_time": localtime(comment.creation_time).isoformat()
            }
            for comment in post.comments.all().order_by("creation_time") 
        ]

        data.append({
            "id": post.id,
            "text": post.text,
            "user_id": post.user.id,
            "user_fullname": f"{post.user.first_name} {post.user.last_name}",
            "creation_time": localtime(post.creation_time).isoformat(),
            "comments": comments
        })

    return JsonResponse({"posts": data})


def add_comment(request):
    # Check if user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    """Handles AJAX request to add a new comment."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    post_id = request.POST.get("post_id")
    comment_text = request.POST.get("comment_text")

    if not post_id or not comment_text:
        return JsonResponse({"error": "Missing required parameters."}, status=400)
    
    try:
        post_id_int = int(post_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid post_id'}, status=400)

    try:
        post = Post.objects.get(id=post_id_int)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=400)


    new_comment = Comment.objects.create(
        text=comment_text,
        user=request.user,
        post=post,
        creation_time=timezone.now()
    )

    comment_data = {
        "id": new_comment.id,
        "text": new_comment.text,
        "user_id": new_comment.user.id,
        "user_fullname": f"{new_comment.user.first_name} {new_comment.user.last_name}",
        "creation_time": localtime(new_comment.creation_time).isoformat(),
    }

    return JsonResponse({"success": True, "comment": comment_data})

