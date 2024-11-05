import os
import django
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diary_project.settings')
django.setup()
from diary.models import Achievement
# Initial achievements data
def create_initial_achievements():
    """Create the initial set of achievements"""
    achievements = [
        # Entry count achievements
        {
            'name': 'First Steps',
            'description': 'Created your first time travel diary entry',
            'category': 'entries',
            'required_entries': 1
        },
        {
            'name': 'Seasoned Traveler',
            'description': 'Created 10 diary entries',
            'category': 'entries',
            'required_entries': 10
        },
        {
            'name': 'Chrono Master',
            'description': 'Created 50 diary entries',
            'category': 'entries',
            'required_entries': 50
        },
        
        # Time period achievements
        {
            'name': 'Time Tourist',
            'description': 'Visited 5 different time periods',
            'category': 'time_periods',
            'required_time_periods': 5
        },
        {
            'name': 'History Hunter',
            'description': 'Visited 10 different time periods',
            'category': 'time_periods',
            'required_time_periods': 10
        },
        {
            'name': 'Timeline Explorer',
            'description': 'Visited 20 different time periods',
            'category': 'time_periods',
            'required_time_periods': 20
        },
        
        # Streak achievements
        {
            'name': 'Time Commitment',
            'description': 'Maintained a 7-day entry streak',
            'category': 'streaks',
            'required_streak': 7
        },
        {
            'name': 'Temporal Dedication',
            'description': 'Maintained a 30-day entry streak',
            'category': 'streaks',
            'required_streak': 30
        },
    ]
    
    for achievement_data in achievements:
        _, status = Achievement.objects.get_or_create(
            name=achievement_data['name'],
            defaults=achievement_data
        )
        print(status)


if __name__ == "__main__":
    create_initial_achievements()