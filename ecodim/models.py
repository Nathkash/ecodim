from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date


class User(AbstractUser):
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('moniteur', 'Moniteur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='moniteur')
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='moniteurs/', blank=True, null=True)

    def is_president(self):
        return self.role == 'president'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"


class Classe(models.Model):
    NOM_CHOICES = [
        ('A', 'Classe A (0-7 ans)'),
        ('B', 'Classe B (8 ans et +)'),
    ]
    nom = models.CharField(max_length=1, choices=NOM_CHOICES, unique=True)
    description = models.TextField(blank=True)
    moniteurs = models.ManyToManyField(
        User,
        related_name='classes_assignees',
        blank=True,
        limit_choices_to={'role': 'moniteur'}
    )

    def __str__(self):
        return self.get_nom_display()


class Enfant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    photo = models.ImageField(upload_to='enfants/', blank=True, null=True)
    nom_parent = models.CharField(max_length=100, blank=True)
    telephone_parent = models.CharField(max_length=20, blank=True)
    date_inscription = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    @property
    def age(self):
        today = date.today()
        delta = today - self.date_naissance
        return delta.days // 365

    @property
    def classe(self):
        if self.age <= 7:
            return Classe.objects.get(nom='A')
        else:
            return Classe.objects.get(nom='B')

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.age} ans)"

    class Meta:
        ordering = ['nom', 'prenom']


class Lecon(models.Model):
    STATUT_CHOICES = [
        ('a_venir', 'À venir'),
        ('donnee', 'Donnée'),
        ('reportee', 'Reportée'),
    ]
    titre = models.CharField(max_length=200)
    theme = models.CharField(max_length=200, blank=True)
    reference_biblique = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='lecons')
    moniteur_assigne = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='lecons_assignees'
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_venir')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='lecons_creees'
    )

    def __str__(self):
        return f"{self.titre} - {self.date} ({self.classe})"

    class Meta:
        ordering = ['-date']


class Seance(models.Model):
    date = models.DateField(unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Séance du {self.date.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-date']


class PresenceEnfant(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='presences_enfants')
    enfant = models.ForeignKey(Enfant, on_delete=models.CASCADE, related_name='presences')
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('seance', 'enfant')

    def __str__(self):
        statut = "✓" if self.present else "✕"
        return f"{statut} {self.enfant} - {self.seance}"


class PresenceMoniteur(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='presences_moniteurs')
    moniteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presences')
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('seance', 'moniteur')

    def __str__(self):
        statut = "✓" if self.present else "✕"
        return f"{statut} {self.moniteur} - {self.seance}"

