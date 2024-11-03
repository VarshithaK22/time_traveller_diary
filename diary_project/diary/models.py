from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class DiaryEntry(models.Model):
    MOOD_CHOICES = [
    ('happy', 'Happy 😊'),
    ('excited', 'Excited 🎉'),
    ('scared', 'Scared 😨'),
    ('neutral', 'Neutral 😐'),
    ('anxious', 'Anxious 😰'),
    ('amazed', 'Amazed 🤩')
]
     
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_of_journey = models.DateField()
    location = models.CharField(max_length=200)

    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entry_detail', kwargs={'pk': self.pk})