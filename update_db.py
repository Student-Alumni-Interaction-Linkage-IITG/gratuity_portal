import os
import sys
import django
import csv

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

# Strict department mappings as requested
DEPT_MAPPING = {
    'BSBE': 'Biosciences and Bioengineering',
    'Biosciences and Bioengineering': 'Biosciences and Bioengineering',
    'Chemical': 'Chemical Engineering',
    'Chemical Engineering': 'Chemical Engineering',
    'Chemistry': 'Chemistry',
    'Civil': 'Civil Engineering',
    'Civil Engineering': 'Civil Engineering',
    'CSE': 'Computer Science and Engineering',
    'Computer Science and Engineering': 'Computer Science and Engineering',
    'Design': 'Design',
    'Electrical': 'Electronics and Electrical Engineering',
    'Electronics and Electrical Engineering': 'Electronics and Electrical Engineering',
    'HSS': 'Humanities and Social Sciences',
    'Humanities and Social Sciences': 'Humanities and Social Sciences',
    'Mathematics': 'Mathematics',
    'Mechanical': 'Mechanical Engineering',
    'Mechanical Engineering': 'Mechanical Engineering',
    'Physics': 'Physics',
    'DS&AI': 'DS&AI'  # Kept as is since it wasn't in the strict list but is in the CSV
}

def import_csv(file_path):
    print(f"Reading CSV from {file_path}...")
    added = 0
    updated = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = (row.get('email') or '').strip()
            name = (row.get('name') or '').strip()
            dept_raw = (row.get('department') or '').strip()
            image_url = (row.get('image_url') or '').strip()
            profile_url = (row.get('url') or '').strip()
            
            if not name:
                continue
                
            # Clean email (fix the mathematical dot issue)
            email = email.replace('⋅', '.').replace('·', '.')
            if not email:
                email = None # Handle empty email
                
            # Map department to strict naming convention
            dept = DEPT_MAPPING.get(dept_raw, dept_raw)
            
            # Create or update professor
            if email:
                prof, created = Professor.objects.get_or_create(email=email, defaults={
                    'name': name,
                    'department': dept,
                    'image_url': image_url,
                    'url': profile_url
                })
                if not created:
                    prof.name = name
                    prof.department = dept
                    if image_url:
                        prof.image_url = image_url
                    if profile_url:
                        prof.url = profile_url
                    prof.save()
                    updated += 1
                else:
                    added += 1
            else:
                # If no email, check by name
                prof, created = Professor.objects.get_or_create(name=name, defaults={
                    'department': dept,
                    'image_url': image_url,
                    'url': profile_url
                })
                if not created:
                    prof.department = dept
                    if image_url:
                        prof.image_url = image_url
                    if profile_url:
                        prof.url = profile_url
                    prof.save()
                    updated += 1
                else:
                    added += 1

    # Finally, clean up any existing database records to use the strict names
    for p in Professor.objects.all():
        mapped_dept = DEPT_MAPPING.get(p.department)
        if mapped_dept and p.department != mapped_dept:
            print(f"Updating department for {p.name}: {p.department} -> {mapped_dept}")
            p.department = mapped_dept
            p.save()

    print(f"\nDone! Added {added} new professors and updated {updated} existing ones.")
    print("All departments have been strictly renamed to your convention.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import_csv(sys.argv[1])
    else:
        print("Please provide the path to the CSV file.")
        print("Usage: python update_db.py Professor-2026-09-01.csv")
