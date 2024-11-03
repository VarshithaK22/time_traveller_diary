import os
import django
from faker import Faker
import random


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diary_project.settings')
django.setup()
from diary.models import DiaryEntry
from django.contrib.auth.models import User
# Initialize Faker
fake = Faker()

# Get all users (assuming you already have some users in your database)
users = list(User.objects.all())
DiaryEntry.objects.all().delete()
if not users:
    raise Exception("No users found in the database. Add some users first.")
def generate_time_travel_context():
    eras = [
        "Ancient Egypt, during the reign of Pharaoh Khufu",
        "The Viking Age, at a bustling seaside village",
        "The Italian Renaissance, among artists like Leonardo da Vinci",
        "The future, in a high-tech utopian society on Mars",
        "The Jurassic period, surrounded by towering dinosaurs",
        "Victorian London, amidst the fog and mystery",
        "A parallel dimension where time flows backward",
        "Medieval Japan, at the height of samurai culture",
        "An alien planet with surreal, crystalline landscapes",
        "The Roaring Twenties, in a lively speakeasy"
    ]
    discoveries = [
        "an ancient artifact that holds a powerful secret",
        "a mysterious creature with the ability to speak all languages",
        "a hidden portal that connects different timelines",
        "a lost civilization with advanced technology",
        "a coded message from another time traveler",
        "a prophecy that foretells an upcoming paradox",
        "an enchanted forest that defies the laws of physics",
        "a historical figure who recognizes the time traveler",
        "a scientific experiment gone wrong, altering reality",
        "a floating city that exists outside of time itself"
    ]
    encounters = [
        "a wise old oracle who knows the future",
        "a group of rebels fighting to change history",
        "a benevolent AI that governs the future society",
        "an alien ambassador with cryptic warnings",
        "a rival time traveler trying to sabotage the mission",
        "a band of time pirates seeking lost treasures",
        "a knight who believes the time traveler is a wizard",
        "a secret society that guards the timeline",
        "a lost explorer from another era",
        "a ghostly apparition seeking closure"
    ]

    return {
        "era": random.choice(eras),
        "discovery": random.choice(discoveries),
        "encounter": random.choice(encounters)
    }

# Create 500 sample diary entries with themed data
for _ in range(500):
    context = generate_time_travel_context()
    title = f"Adventure in {context['era']}"
    content = (
        f"On this journey to {context['era']}, I made a remarkable discovery: {context['discovery']}. "
        f"My encounter with {context['encounter']} left a lasting impression. "
        f"The experience was both exhilarating and full of peril, as the past and future collided."
    )
    date_of_journey = fake.date_between(start_date='-500y', end_date='+500y')
    location = context['era']
    user = random.choice(users)

    DiaryEntry.objects.create(
        title=title,
        content=content,
        date_of_journey=date_of_journey,
        location=location,
        user=user
    )

print("500 themed Time Traveler's Diary entries have been created successfully.")