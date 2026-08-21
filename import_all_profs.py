import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

def import_profs():
    file_path = 'profData.csv'
    if not os.path.exists(file_path):
        file_path = '../profData.csv'
        
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        created_count = 0
        
        for row in reader:
            name = row.get('name', '').strip()
            department = row.get('department', '').strip()
            email = row.get('email', '').strip()
            # Clean up emails if needed
            email = email.replace(' ', '')
            
            image_url = row.get('image_url', '').strip()
            url = row.get('url', '').strip()
            
            if not email or not name:
                continue
                
            prof, created = Professor.objects.update_or_create(
                email=email,
                defaults={
                    'name': name,
                    'department': department,
                    'image_url': image_url,
                    'url': url
                }
            )
            if created:
                created_count += 1
                
    print(f"Successfully imported/updated professors. Total created: {created_count}")

if __name__ == '__main__':
    import_profs()
