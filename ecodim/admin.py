from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Classe, Enfant, Lecon, Seance, PresenceEnfant, PresenceMoniteur


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'telephone')
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Écodim', {'fields': ('role', 'telephone', 'photo')}),
    )


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    filter_horizontal = ('moniteurs',)


@admin.register(Enfant)
class EnfantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'age', 'classe', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom', 'prenom')


@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'classe', 'moniteur_assigne', 'statut')
    list_filter = ('statut', 'classe')
    search_fields = ('titre', 'theme')


@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ('date',)


@admin.register(PresenceEnfant)
class PresenceEnfantAdmin(admin.ModelAdmin):
    list_display = ('enfant', 'seance', 'present')
    list_filter = ('present', 'seance')


@admin.register(PresenceMoniteur)
class PresenceMoniteurAdmin(admin.ModelAdmin):
    list_display = ('moniteur', 'seance', 'present')
    list_filter = ('present',)

