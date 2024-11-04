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
from .forms import DiaryEntrySearchForm
from django.db.models import Q
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
    user = request.user  
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)


class EntryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'home.html'
    context_object_name = 'entries'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) 
            )
        time_period = self.request.GET.get('time_period')
        if time_period:
            queryset = queryset.filter(time_period=time_period)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DiaryEntrySearchForm(self.request.GET)
        return context
