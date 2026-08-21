import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Professor

@user_passes_test(lambda u: u.is_superuser)
def manage_professors(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('manage_professors')
            
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            created_count = 0
            updated_count = 0
            
            for row in reader:
                # Based on user schema: id,name,department,email,image_url,url
                name = row.get('name', '').strip()
                department = row.get('department', '').strip()
                email = row.get('email', '').strip()
                # Some emails might have weird spacing like 'email @ domain'
                email = email.replace(' ', '').replace('⋅', '.')
                
                image_url = row.get('image_url', '').strip()
                url = row.get('url', '').strip()
                
                if not email or not name:
                    continue # Skip invalid rows
                    
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
                else:
                    updated_count += 1
                    
            messages.success(request, f'Successfully imported! {created_count} new professors created, {updated_count} updated.')
        except Exception as e:
            messages.error(request, f'Error parsing CSV: {str(e)}')
            
        return redirect('manage_professors')
        
    # GET request: display professors and upload form
    professors = Professor.objects.all().order_by('name')
    return render(request, 'manage_professors.html', {'professors': professors})
