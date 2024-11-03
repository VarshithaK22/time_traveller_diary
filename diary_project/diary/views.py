from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from .models import DiaryEntry

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)        
        if user_form.is_valid():
            user = user_form.save()            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Change to your home view
    else:
        user_form = UserRegistrationForm()    
    return render(request, 'register.html', {
        'user_form': user_form,
    })

@login_required
def profile(request):
    return render(request, 'profile.html')


class EntryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'home.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)
