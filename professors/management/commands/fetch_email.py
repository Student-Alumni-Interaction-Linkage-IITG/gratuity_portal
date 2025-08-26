import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from professors.models import Professor


class Command(BaseCommand):
    help = "Fetch emails from professor URLs and update database"

    def handle(self, *args, **kwargs):
        professors = Professor.objects.filter(email__in=[None, ""]).exclude(url__isnull=True).exclude(url="")

        for prof in professors:
            try:
                self.stdout.write(f"🔍 Scraping {prof.url} ...")

                response = requests.get(prof.url, timeout=10)
                if response.status_code != 200:
                    self.stdout.write(self.style.WARNING(f"⚠️ Could not fetch {prof.url}"))
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                # Find the first span with class 'text-info'
                email_span = soup.find("span", class_="text-info")

                if email_span:
                    email = email_span.get_text(strip=True)

                    prof.email = email
                    prof.save(update_fields=["email"])
                    self.stdout.write(self.style.SUCCESS(f"✅ {prof.name} -> {email}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ No span.text-info found for {prof.name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error for {prof.name}: {e}"))
