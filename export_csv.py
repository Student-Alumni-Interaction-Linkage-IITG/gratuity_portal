import os
import sys
import django
import csv

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

def export_to_csv():
    # Fetch all professors from the database (Ramtej is already deleted, and departments are strict)
    profs = Professor.objects.all().order_by('id')
    
    file_name = 'updated_professors.csv'
    
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow([
            'id', 'name', 'department', 'email', 
            'email_notifications_enabled', 'image_url', 'url'
        ])
        
        for p in profs:
            writer.writerow([
                p.id,
                p.name,
                p.department,
                p.email if p.email else '',
                p.email_notifications_enabled,
                p.image_url if p.image_url else '',
                p.url if p.url else ''
            ])
            
    print(f"Successfully exported {profs.count()} professors to {file_name}!")

if __name__ == "__main__":
    export_to_csv()
