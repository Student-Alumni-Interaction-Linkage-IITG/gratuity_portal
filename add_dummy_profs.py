import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

departments = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Mechanical Engineering']
first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Jessica', 'William', 'Ashley', 'James', 'Amanda', 'Charles', 'Melissa', 'Joseph', 'Stephanie']
last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin']

print("Creating 50 dummy professors...")
for i in range(50):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    name = f"Dr. {first_name} {last_name}"
    dept = random.choice(departments)
    email = f"{first_name.lower()}.{last_name.lower()}{i}@iitg.ac.in"
    
    Professor.objects.create(
        name=name,
        department=dept,
        email=email
    )
print("Done!")
