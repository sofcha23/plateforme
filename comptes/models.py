from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle pour les Services (BV, SDCTR, SDEDS, SDEP, Direction)
class Service(models.Model):
    nom = models.CharField(max_length=100, unique=True)  # Le nom complet du service
    code = models.CharField(max_length=10, unique=True)  # Un code court (ex: "BV", "SDCTR")

    def __str__(self):
        return f"{self.code} - {self.nom}"

    class Meta:
        ordering = ['code']  # Pour les trier par code par défaut

# Modèle d'Utilisateur Personnalisé qui étend le modèle standard de Django
class Utilisateur(AbstractUser):
    # Lie l'utilisateur à un service. 'null=True' est temporaire pour les superadmins.
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    # Champ pour différencier un simple membre d'un admin de service.
    est_admin_service = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.service})"