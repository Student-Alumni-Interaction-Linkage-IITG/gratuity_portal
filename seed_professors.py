import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

def seed():
    dummy_data = [
        {
            "name": "Dr. Alan Turing",
            "department": "Computer Science",
            "email": "alan.turing@example.com",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a1/Alan_Turing_Aged_16.jpg",
            "url": "https://en.wikipedia.org/wiki/Alan_Turing"
        },
        {
            "name": "Dr. Marie Curie",
            "department": "Physics",
            "email": "marie.curie@example.com",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Marie_Curie_c._1920s.jpg",
            "url": "https://en.wikipedia.org/wiki/Marie_Curie"
        },
        {
            "name": "Dr. Richard Feynman",
            "department": "Physics",
            "email": "richard.feynman@example.com",
            "image_url": "https://upload.wikimedia.org/wikipedia/en/4/42/Richard_Feynman_Nobel.jpg",
            "url": "https://en.wikipedia.org/wiki/Richard_Feynman"
        },
        {
            "name": "Dr. Ada Lovelace",
            "department": "Mathematics",
            "email": "ada.lovelace@example.com",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Ada_Lovelace_portrait.jpg",
            "url": "https://en.wikipedia.org/wiki/Ada_Lovelace"
        }
    ]

    for data in dummy_data:
        prof, created = Professor.objects.get_or_create(
            email=data["email"],
            defaults=data
        )
        if created:
            print(f"Created Professor: {prof.name}")
        else:
            print(f"Professor already exists: {prof.name}")
            
    print("\nDummy data seeding complete!")

if __name__ == '__main__':
    seed()
