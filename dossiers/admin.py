from django.contrib import admin
from .models import Dossier

class DossierAdmin(admin.ModelAdmin):
    # Liste des colonnes affichées
    list_display = (
        'code', 
        'denomination_commerciale', 
        'fabricant',
        'statut', 
        'date_limite', 
        'assigne_a', 
        'est_en_retard'
    )
    
    # Filtres disponibles
    list_filter = (
        'statut', 
        'date_limite', 
        'type_demande',
        'assigne_a__service'  # Filtre par service
    )
    
    # Recherche
    search_fields = (
        'code', 
        'denomination_commerciale', 
        'fabricant',
        'pays_origine'
    )
    
    # Organisation des champs dans le formulaire de détail
    fieldsets = (
        ('Informations Générales', {
            'fields': (
                'code', 
                'denomination_commerciale',
                'fabricant',
                'pays_origine',
                'type_demande'
            )
        }),
        ('Dates Importantes', {
            'fields': (
                'date_depot',
                'date_reception',
                'date_limite',
                'date_bv',
                'date_notification'
            )
        }),
        ('Évaluation et Suivi', {
            'fields': (
                'statut',
                'evaluateur',
                'date_fin_evaluation',
                'verificateur',
                'date_fin_verification',
                'reserves',
                'certificat_ce'
            )
        }),
        ('Assignation', {
            'fields': (
                'assigne_a',
                'cree_par'
            )
        }),
    )
    
    # Fonction pour la colonne "est en retard"
    def est_en_retard(self, obj):
        return obj.est_en_retard()
    est_en_retard.boolean = True
    est_en_retard.short_description = 'En retard ?'

admin.site.register(Dossier, DossierAdmin)