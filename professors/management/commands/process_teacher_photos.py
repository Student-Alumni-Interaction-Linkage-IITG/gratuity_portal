from django.core.management.base import BaseCommand
from professors.models import Professor
from professors.utils import process_teacher_photo
import sys

class Command(BaseCommand):
    help = 'Processes all existing teacher photos using OpenCV face detection'

    def handle(self, *args, **options):
        self.stdout.write("Processing teacher photos...\n")
        
        professors = Professor.objects.exclude(profile_picture='').exclude(profile_picture__isnull=True)
        total = professors.count()
        
        if total == 0:
            self.stdout.write("No professors with profile pictures found.")
            return

        completed = 0
        failed = 0
        skipped = 0

        for i, prof in enumerate(professors, 1):
            if prof.processed_profile_picture:
                self.stdout.write(f"[{i}/{total}] {prof.name:<30} (Skipped - already processed)")
                skipped += 1
                continue
                
            try:
                success = process_teacher_photo(prof)
                if success:
                    self.stdout.write(self.style.SUCCESS(f"[{i}/{total}] {prof.name:<30} OK"))
                    completed += 1
                else:
                    self.stdout.write(self.style.ERROR(f"[{i}/{total}] {prof.name:<30} FAIL (Processing failed)"))
                    failed += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[{i}/{total}] {prof.name:<30} FAIL ({str(e)})"))
                failed += 1
                
        self.stdout.write("\n" + "="*30)
        self.stdout.write(f"Completed: {completed}")
        self.stdout.write(f"Failed: {failed}")
        self.stdout.write(f"Skipped: {skipped}")
