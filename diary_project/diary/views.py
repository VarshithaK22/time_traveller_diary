from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
)
from django.contrib import messages
from .models import DiaryEntry, UserAchievement, Achievement, UserProgress
from .forms import DiaryEntrySearchForm
from django.db.models import Q
from django.db.models import Count
from collections import defaultdict


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")  # Change to your home view
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        "register.html",
        {
            "user_form": user_form,
        },
    )


@login_required
def profile(request):
    user = request.user

    # Get user's progress
    progress, _ = UserProgress.objects.get_or_create(user=user)

    # Get earned achievements
    earned_achievements = UserAchievement.objects.filter(user=user).select_related(
        "achievement"
    )

    # Get all achievements and organize them by category
    all_achievements = Achievement.objects.all()
    achievements_by_category = defaultdict(list)

    for achievement in all_achievements:
        # Calculate progress percentage for each achievement
        progress_percent = 0
        if achievement.required_entries > 0:
            progress_percent = min(
                100, (progress.total_entries / achievement.required_entries) * 100
            )
        elif achievement.required_time_periods > 0:
            progress_percent = min(
                100,
                (progress.unique_time_periods / achievement.required_time_periods)
                * 100,
            )
        elif achievement.required_streak > 0:
            progress_percent = min(
                100, (progress.longest_streak / achievement.required_streak) * 100
            )

        # Check if achievement is earned
        is_earned = earned_achievements.filter(achievement=achievement).exists()

        # Add achievement info to category list
        achievements_by_category[achievement.get_category_display()].append(
            {
                "achievement": achievement,
                "is_earned": is_earned,
                "progress_percent": int(progress_percent),
                "earned_at": next(
                    (
                        ea.earned_at
                        for ea in earned_achievements
                        if ea.achievement_id == achievement.id
                    ),
                    None,
                ),
            }
        )

    # Get user's diary statistics
    diary_stats = {
        "total_entries": progress.total_entries,
        "unique_time_periods": progress.unique_time_periods,
        "current_streak": progress.current_streak,
        "longest_streak": progress.longest_streak,
        "last_entry_date": progress.last_entry_date,
    }

    # Get most visited time periods
    most_visited_periods = (
        DiaryEntry.objects.filter(user=user)
        .values("time_period")
        .annotate(visit_count=Count("time_period"))
        .order_by("-visit_count")[:5]
    )

    # Get the display names for time periods
    time_period_dict = dict(DiaryEntry.TIME_PERIOD_CHOICES)
    for period in most_visited_periods:
        period["display_name"] = time_period_dict.get(period["time_period"])

    # Recent entries
    recent_entries = DiaryEntry.objects.filter(user=user).order_by("-date_of_journey")[
        :5
    ]

    context = {
        "user": user,
        "diary_stats": diary_stats,
        "achievements_by_category": dict(achievements_by_category),
        "most_visited_periods": most_visited_periods,
        "recent_entries": recent_entries,
        "total_achievements": all_achievements.count(),
        "earned_achievements": earned_achievements.count(),
        "achievement_progress": (
            round((earned_achievements.count() / all_achievements.count()) * 100)
            if all_achievements.count() > 0
            else 0
        ),
    }

    return render(request, "profile.html", context)


class EntryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = "home.html"
    context_object_name = "entries"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        time_period = self.request.GET.get("time_period")
        if time_period:
            queryset = queryset.filter(time_period=time_period)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = DiaryEntrySearchForm(self.request.GET)
        return context
