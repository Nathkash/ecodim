from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Crée le compte président par défaut'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='president').exists():
            User.objects.create_superuser(
                username='president',
                password='ecodim2024',
                first_name='Président',
                last_name='Écodim',
                role='president'
            )
            self.stdout.write(self.style.SUCCESS('✅ Compte président créé !'))
            self.stdout.write(self.style.WARNING('⚠️  Changez le mot de passe après connexion !'))
        else:
            self.stdout.write('ℹ️  Compte président déjà existant')