# accounts/migrations/0002_add_sample_users.py
from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_sample_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    # Define sample users
    sample_users = [
        {'username': 'admin1', 'password': make_password('Admin1'), 'email': 'admin1@example.com', 'is_superuser': True, 'is_staff': True},
        {'username': 'user1', 'password': make_password('User1pass'), 'email': 'user1@example.com'},
        {'username': 'user2', 'password': make_password('User2pass'), 'email': 'user2@example.com'},
        {'username': 'user3', 'password': make_password('User3pass'), 'email': 'user3@example.com'},
    ]

    # Create users if they don't already exist
    for user_data in sample_users:
        if not User.objects.filter(username=user_data['username']).exists():
            User.objects.create(**user_data)

def delete_sample_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    usernames = ['admin1', 'user1', 'user2', 'user3']
    User.objects.filter(username__in=usernames).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),  # Update to your actual last migration file
    ]

    operations = [
        migrations.RunPython(create_sample_users, delete_sample_users),
    ]
