from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.views.generic.detail import DetailView

class EntryCreateView(View):
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

class EntryDetailView(DetailView):
    model = DiaryEntry
    template_name = 'entry/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context