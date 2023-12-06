from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserDeleteForm

def register(request):
    if request.method == 'POST': 
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:   
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required #prevent acess to profile if logged out
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,     request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account Info Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def delete_user(request):
    if request.method == 'POST':
        form = UserDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirmation']:
            user = request.user
            user.delete()
            logout(request)
            return redirect('home')  # Redirect to the home page or a success page
    else:
        form = UserDeleteForm()

    return render(request, 'delete_user.html', {'form': form})