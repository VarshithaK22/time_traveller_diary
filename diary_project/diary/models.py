from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
import uuid
from datetime import datetime
import os
def get_valid_name( name):
    """Returns a filename that's cleaned and unique."""
    name = clean_filename(name)
    name_without_extension, extension = os.path.splitext(name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    final_name = f"{name_without_extension}_{timestamp}_{unique_id}{extension}"
    return final_name

def clean_filename( name):
    """Cleans the filename by removing special characters and spaces."""
    name_without_extension, extension = os.path.splitext(name)
    cleaned_name = slugify(name_without_extension)
    return f"{cleaned_name}{extension.lower()}"

def user_directory_path(instance, filename):
    file_name = get_valid_name(filename)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user.id, file_name)

class DiaryEntry(models.Model):
    MOOD_CHOICES = [
        ("happy", "Happy 😊"),
        ("excited", "Excited 🎉"),
        ("scared", "Scared 😨"),
        ("neutral", "Neutral 😐"),
        ("anxious", "Anxious 😰"),
        ("amazed", "Amazed 🤩"),
    ]
    TIME_PERIOD_CHOICES = [
        # Ancient Civilizations
        ("ancient_egypt", "Ancient Egypt (3100 BCE - 30 BCE)"),
        ("ancient_rome", "Ancient Rome (753 BCE - 476 CE)"),
        ("ancient_greece", "Ancient Greece (800 BCE - 146 BCE)"),
        ("ancient_china", "Ancient China (2100 BCE - 221 BCE)"),
        # Medieval Period
        ("medieval_europe", "Medieval Europe (476 CE - 1500 CE)"),
        ("medieval_japan", "Medieval Japan (1185 CE - 1603 CE)"),
        ("medieval_arabia", "Islamic Golden Age (750 CE - 1258 CE)"),
        # Modern History
        ("renaissance", "Renaissance (1300 CE - 1700 CE)"),
        ("industrial_revolution", "Industrial Revolution (1760 CE - 1840 CE)"),
        ("modern_age", "Modern Age (1900 CE - Present)"),
        # Near Future (2024-2100)
        ("near_future_earth", "Early Space Age Earth (2024-2050)"),
        ("lunar_colonization", "Lunar Colonies Era (2040-2080)"),
        ("solar_system_expansion", "Solar System Expansion (2060-2100)"),
        # Mars Era (2100-2200)
        ("early_mars", "Early Mars Settlement (2100-2130)"),
        ("mars_terraform", "Mars Terraforming Period (2130-2170)"),
        ("established_mars", "Established Mars Civilization (2170-2200)"),
        # Solar System Era (2200-2500)
        ("asteroid_mining", "Asteroid Belt Colonization (2200-2300)"),
        ("gas_giant_stations", "Gas Giant Stations Era (2300-2400)"),
        ("kuiper_outposts", "Kuiper Belt Outposts (2400-2500)"),
        # Interstellar Era (2500-3000)
        ("proxima_colonization", "Proxima Centauri Colony (2500-2600)"),
        ("stellar_expansion", "Multi-Star Expansion (2600-2800)"),
        ("galactic_pioneers", "Early Galactic Age (2800-3000)"),
        # Far Future Eras (3000+)
        ("galactic_civilization", "Galactic Civilization (3000-5000)"),
        ("interstellar_empire", "Interstellar Empire (5000-10000)"),
        ("cosmic_age", "Cosmic Civilization (10000+)"),
        # Alternative Future Paths
        ("post_singularity", "Post-Singularity Era"),
        ("digital_consciousness", "Digital Consciousness Age"),
        ("bio_synthetic_fusion", "Bio-Synthetic Fusion Era"),
        ("quantum_realm", "Quantum Realm Civilization"),
        ("parallel_worlds", "Multi-Dimensional Society"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_of_journey = models.DateField()
    location = models.CharField(max_length=200)

    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)

    time_period = models.CharField(
        max_length=50,
        choices=TIME_PERIOD_CHOICES,
        default="modern_age",
        help_text="The historical or future time period of this entry",
    )

    destination_date = models.DateField(
        null=True, help_text="Specific year within the time period (optional)"
    )

    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"pk": self.pk})


User = get_user_model()


class Achievement(models.Model):
    """Define the various achievements that users can earn"""

    CATEGORY_CHOICES = [
        ("entries", "Diary Entries"),
        ("time_periods", "Time Periods"),
        ("streaks", "Time Travel Streaks"),
        ("special", "Special Achievements"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.ImageField(upload_to=settings.ACHIEVEMENT_ROOT, null=True, blank=True)

    # Requirements for earning
    required_entries = models.IntegerField(default=0)
    required_time_periods = models.IntegerField(default=0)
    required_streak = models.IntegerField(default=0)

    class Meta:
        ordering = ["category", "required_entries", "required_time_periods"]

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Track achievements earned by users"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "achievement"]


class UserProgress(models.Model):
    """Track user progress towards achievements"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_entries = models.IntegerField(default=0)
    unique_time_periods = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_entry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Progress for {self.user.username}"


# Signal handlers for achievement tracking
@receiver(post_save, sender="diary.DiaryEntry")
def update_user_progress(sender, instance, created, **kwargs):
    """Update user progress when a new diary entry is created"""
    if not created:
        return

    progress, _ = UserProgress.objects.get_or_create(user=instance.user)

    # Update total entries
    progress.total_entries += 1

    # Update unique time periods
    unique_periods = (
        sender.objects.filter(user=instance.user)
        .values("time_period")
        .distinct()
        .count()
    )
    progress.unique_time_periods = unique_periods

    # Update streak
    today = timezone.now().date()
    if progress.last_entry_date:
        days_diff = (today - progress.last_entry_date).days
        if days_diff == 1:  # Consecutive day
            progress.current_streak += 1
            progress.longest_streak = max(
                progress.current_streak, progress.longest_streak
            )
        elif days_diff > 1:  # Streak broken
            progress.current_streak = 1
    else:
        progress.current_streak = 1

    progress.last_entry_date = today
    progress.save()

    check_achievements(instance.user)


def check_achievements(user):
    """Check and award any newly earned achievements"""
    progress = UserProgress.objects.get(user=user)
    earned_achievements = UserAchievement.objects.filter(user=user).values_list(
        "achievement_id", flat=True
    )

    # Get all achievements that haven't been earned yet
    potential_achievements = Achievement.objects.exclude(id__in=earned_achievements)

    for achievement in potential_achievements:
        earned = False

        # Check entry count achievements
        if achievement.required_entries > 0:
            earned = progress.total_entries >= achievement.required_entries

        # Check time period achievements
        if achievement.required_time_periods > 0:
            earned = progress.unique_time_periods >= achievement.required_time_periods

        # Check streak achievements
        if achievement.required_streak > 0:
            earned = progress.longest_streak >= achievement.required_streak

        if earned:
            UserAchievement.objects.create(user=user, achievement=achievement)
