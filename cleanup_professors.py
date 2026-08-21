import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

def cleanup():
    emails_to_delete = [
        "alan.turing@example.com",
        "marie.curie@example.com",
        "richard.feynman@example.com",
        "ada.lovelace@example.com"
    ]
    
    deleted_count, _ = Professor.objects.filter(email__in=emails_to_delete).delete()
    print(f"Cleanup complete! Deleted {deleted_count} dummy professor(s).")

if __name__ == '__main__':
    cleanup()
