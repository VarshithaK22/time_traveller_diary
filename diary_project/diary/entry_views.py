from django.views import View
from django.shortcuts import render, redirect
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class EntryCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = DiaryEntryForm()
        return render(request, 'entry/form.html', {'form': form})

    def post(self, request):
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('home')
        return render(request, 'entry/form.html', {'form': form})

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = DiaryEntry
    template_name = 'entry/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'entry/update.html'

    def get_success_url(self):
        return reverse_lazy('entry_detail', kwargs={'pk': self.object.pk})

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = DiaryEntry
    template_name = 'entry/delete.html'
    success_url = reverse_lazy('home')  # Redirect to the list view after deletion