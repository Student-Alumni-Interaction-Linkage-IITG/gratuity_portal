import csv
from django.core.management.base import BaseCommand
from professors.models import Professor  # adjust if model name is different

class Command(BaseCommand):
    help = "Import professors from CSV"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="/profData.csv")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        with open(csv_file, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                Professor.objects.update_or_create(
                    name=row["name"],
                    defaults={
                        "department": row["department"],
                        "email": row["email"],  
                        "image_url": row["image_url"],
                        "url": row["url"],
                    },
                )
        self.stdout.write(self.style.SUCCESS("Professors imported successfully!"))
