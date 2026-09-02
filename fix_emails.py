import os
import sys
import django

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

profs = Professor.objects.all()
fixed_count = 0
for p in profs:
    old_email = p.email
    if old_email:
        # Replace weird dots like mathematical dots or interpuncts with a standard period
        new_email = old_email.replace('⋅', '.').replace('·', '.')
        if new_email != old_email:
            p.email = new_email
            p.save()
            print(f"Fixed {p.name}: {old_email} -> {new_email}")
            fixed_count += 1

print(f"Done! Fixed {fixed_count} email addresses.")
