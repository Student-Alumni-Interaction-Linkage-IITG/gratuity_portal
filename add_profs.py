import os
import sys
import django

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gratuity_portal.settings')
django.setup()

from professors.models import Professor

data = [
    ("Rhythm Grover", "rhythmgrover@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_rhythm_grover.jpg"),
    ("Shruti Shantiling Phutke", "ssphutke@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/shruti_2026_rz.jpeg"),
    ("Teena Sharma", "teena@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_teena_aug26.jpg"),
    ("Amulya Kumar Mahto", "akmahto@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_amulya_mahto.png"),
    ("Arghyadip Roy", "arghyadip@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_arghyadip_roy.jpg"),
    ("Ayon Borthakur", "ayon.borthakur@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_ayon_borthakur.jpg"),
    ("Chiranjib Sur", "chiranjib@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_chiranjib_sur.jpg"),
    ("Chetan S. Ralekar", "chetan.ralekar@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_chetanRalekar.png"),
    ("Debanga Raj Neog", "dneog@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_debanga_raj_neog.jpg"),
    ("Dipankar Mondal", "mdipankar@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/dipankar_resize.jpg"),
    ("Neeraj Kumar Sharma", "neerajs@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_neeraj_sharma.png"),
    ("Prashant W. Patil", "pwpatil@iitg.ac.in", "DS&AI", "https://www.iitg.ac.in/dsai/images/core_faculty_pics/resize_prashant_wpatil.jpeg"),
]

for name, email, dept, url in data:
    prof, created = Professor.objects.get_or_create(email=email, defaults={'name': name, 'department': dept, 'image_url': url})
    if not created:
        prof.name = name
        prof.department = dept
        prof.image_url = url
        prof.save()
    print(f"{'Created' if created else 'Updated'} {name}")
