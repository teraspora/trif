# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from fract.models import Image

def register(request):
    """ Render a form to allow a new user to register. """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created: {username}.  Please check you can log in ok...')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """ Render a combined form to let a user update user and profile data. """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account updated: {username}.')
            # Serve the profile page by GET request to obviate duplicate POST data
            return redirect('profile') 
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

def add_like(request, img_id):
    """ Handle 'liking' of an image by a user. by updating user's liked images list (stored in profile).
        This is a ManyToManyField so the image's profile_set will also be updated.
        When done, load the image's detail view page.
    """
    user = request.user
    img = get_object_or_404(Image, pk=img_id)
    user.profile.liked_images.add(img)
    user.profile.save()
    return redirect(f'/image/{img_id}')
