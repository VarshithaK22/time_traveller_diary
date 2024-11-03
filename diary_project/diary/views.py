from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm#, ProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid():
        # and profile_form.is_valid():
            user = user_form.save()
            # user.profile.date_of_birth = profile_form.cleaned_data.get('date_of_birth')
            user.profile.save()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Change to your home view
    else:
        user_form = UserRegistrationForm()
        # profile_form = ProfileForm()
    
    return render(request, 'register.html', {
        'user_form': user_form,
        # 'profile_form': profile_form
    })

@login_required
def profile(request):
    return render(request, 'profile.html')