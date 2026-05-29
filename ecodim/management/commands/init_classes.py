from django.core.management.base import BaseCommand
from ecodim.models import Classe


class Command(BaseCommand):
    def handle(self, *args, **options):
        classe_a, created_a = Classe.objects.get_or_create(
            nom='A',
            defaults={'description': 'Enfant de 0 à 7 ans'}
        )
        classe_b, created_b = Classe.objects.get_or_create(
            nom='B',
            defaults={'description': 'Enfant de 8 ans et plus'}
        )

        if created_a:
            self.stdout.write(self.style.SUCCESS('Classe A créée'))
        else:
            self.stdout.write("Classe A déjà existante")

        if created_b:
            self.stdout.write(self.style.SUCCESS('Classe B créée'))
        else:
            self.stdout.write("Classe B déjà existante")
