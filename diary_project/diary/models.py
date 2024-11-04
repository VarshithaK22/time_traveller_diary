from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
        default='modern_age',
        help_text="The historical or future time period of this entry"
    )
    
    destination_date = models.DateField(
        null=True,
        help_text="Specific year within the time period (optional)"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"pk": self.pk})
