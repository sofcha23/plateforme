from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Service, Utilisateur

# Configuration de l'interface admin pour le modèle Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom')  # Colonnes à afficher dans la liste
    ordering = ('code',)            # Ordre de tri par défaut

# Configuration de l'interface admin pour le modèle Utilisateur personnalisé
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'service', 'est_admin_service', 'is_staff')
    # Filtres disponibles sur le côté droit
    list_filter = ('service', 'est_admin_service', 'is_staff', 'is_superuser')
    
    # Organisation des champs dans le formulaire de détail
    fieldsets = UserAdmin.fieldsets + (
        # Ajout d'une section supplémentaire pour nos champs personnalisés
        ('Informations Métier', {
            'fields': ('service', 'est_admin_service')
        }),
    )
