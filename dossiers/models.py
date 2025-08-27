from django.db import models
from comptes.models import Utilisateur

class Dossier(models.Model):
    # --- Champs de base et identifiants ---
    code = models.CharField(max_length=50, unique=True, verbose_name="Code dossier",  blank=True )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    # --- Statut et Workflow ---
    class StatutDossier(models.TextChoices):
        EN_ATTENTE = 'EA', 'En Attente'
        EN_COURS = 'EC', 'En Cours'
        TERMINE = 'TR', 'Terminé'
        REJETE = 'RJ', 'Rejeté'

    statut = models.CharField(
        max_length=2,
        choices=StatutDossier.choices,
        default=StatutDossier.EN_ATTENTE,
        verbose_name="Statut"
    )
    date_limite = models.DateField(null=True, blank=True, verbose_name="Date limite")

    # --- Relations ---
    assigne_a = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dossiers_assignes',
        verbose_name="Assigné à"
    )
    cree_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='dossiers_crees',
        verbose_name="Créé par"
    )

    # --- Méthodes ---
    def __str__(self):
        return f"{self.code} - {self.statut}"

    def est_en_retard(self):
        from datetime import date
        if self.date_limite and self.statut not in [self.StatutDossier.TERMINE, self.StatutDossier.REJETE]:
            return self.date_limite < date.today()
        return False

    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"
        # Informations générales (tous les services)
    denomination_commerciale = models.CharField(max_length=200, blank=True, verbose_name="Dénomination Commerciale")
    fabricant = models.CharField(max_length=100, blank=True, verbose_name="Fabricant")
    pays_origine = models.CharField(max_length=50, blank=True, verbose_name="Pays d'Origine")
    type_demande = models.CharField(max_length=50, blank=True, verbose_name="Type de demande")
    
    # Champs dates importantes
    date_depot = models.DateField(null=True, blank=True, verbose_name="Date de dépôt")
    date_reception = models.DateField(null=True, blank=True, verbose_name="Date de réception")
    
    # Évaluation
    evaluateur = models.CharField(max_length=100, blank=True, verbose_name="Évaluateur")
    date_fin_evaluation = models.DateField(null=True, blank=True, verbose_name="Date fin évaluation")
    verificateur = models.CharField(max_length=100, blank=True, verbose_name="Vérificateur")
    date_fin_verification = models.DateField(null=True, blank=True, verbose_name="Date fin vérification")
    
    # Références
    numero_bv = models.CharField(max_length=50, blank=True, verbose_name="Numéro BV")
    date_bv = models.DateField(null=True, blank=True, verbose_name="Date BV")
    numero_notification = models.CharField(max_length=50, blank=True, verbose_name="Numéro notification")
    date_notification = models.DateField(null=True, blank=True, verbose_name="Date notification")
    
    # Statut avancé
    reserves = models.TextField(blank=True, verbose_name="Réserves")
    certificat_ce = models.BooleanField(default=False, verbose_name="Certificat CE")
    
    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"