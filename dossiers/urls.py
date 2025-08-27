from django.urls import path
from . import views

urlpatterns = [
    path('mes-dossiers/', views.liste_dossiers, name='liste_dossiers'),
    path('tableau-de-bord/', views.tableau_de_bord_admin, name='tableau_de_bord'),  # Nouvelle ligne
    path('ajouter-dossier/', views.ajouter_dossier, name='ajouter_dossier'),
    path('modifier-dossier/<int:dossier_id>/', views.modifier_dossier, name='modifier_dossier'),
    
]