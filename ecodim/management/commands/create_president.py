from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Crée le compte président par défaut'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='president').exists():
            user = User.objects.create_superuser(
                username='nath_kash',
                password='admin123',
                first_name='Président',
                last_name='Écodim',
                role='president'
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Compte président créé !'))
        else:
            # Met à jour si déjà existant
            user = User.objects.get(username='president')
            user.is_staff = True
            user.is_superuser = True
            user.set_password('ecodim2024')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Compte président mis à jour !'))