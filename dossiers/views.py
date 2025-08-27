from django.shortcuts import render, redirect 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Ajoutez cette ligne
from django.utils import timezone  # Ajoutez cette ligne aussi
from .models import Dossier


@login_required
def liste_dossiers(request):
    utilisateur = request.user
    print(f"UTILISATEUR CONNECTÉ : {utilisateur.username}")  # Debug
    print(f"SERVICE : {utilisateur.service}")  # Debug
    print(f"EST ADMIN : {utilisateur.est_admin_service}")  # Debug

    # Logique de filtrage SIMPLIFIÉE
    if utilisateur.service and utilisateur.service.code == "DIR":
        print("ACCÈS: Super Admin - voir TOUT")  # Debug
        dossiers = Dossier.objects.all()
    else:
        print("ACCÈS: Membre - voir seulement ses dossiers")  # Debug
        dossiers = Dossier.objects.filter(assigne_a=utilisateur)

    print(f"NOMBRE DE DOSSIERS TROUVÉS : {dossiers.count()}")  # Debug
    context = {
        'dossiers': dossiers,
        'utilisateur': utilisateur
    }
    return render(request, 'dossiers/liste_dossiers.html', context)
def test_debug(request):
    print("=== TEST DEBUG ===")
    print("Ce message devrait apparaître dans le terminal")
    print(f"Utilisateur: {request.user}")
    return render(request, 'dossiers/test.html')
# Dans dossiers/views.py
@login_required
def tableau_de_bord_admin(request):
    if not request.user.est_admin_service:
        return redirect('liste_dossiers')
    
    # Logique pour les stats et indicateurs
    # ...
    from django.db.models import Count, Q
from django.utils import timezone

@login_required
def tableau_de_bord_admin(request):
    """
    Tableau de bord réservé aux administrateurs de service
    """
    # Vérification des permissions
    if not request.user.est_admin_service or not request.user.service:
        return redirect('liste_dossiers')
    
    # Récupère tous les dossiers du service
    dossiers_du_service = Dossier.objects.filter(
        assigne_a__service=request.user.service
    )
    
    # Calcul des statistiques
    stats = {
        'total': dossiers_du_service.count(),
        'en_attente': dossiers_du_service.filter(statut='EA').count(),
        'en_cours': dossiers_du_service.filter(statut='EC').count(),
        'termines': dossiers_du_service.filter(statut='TR').count(),
        'en_retard': dossiers_du_service.filter(
            Q(date_limite__lt=timezone.now().date()) &
            ~Q(statut__in=['TR', 'RJ'])
        ).count(),
    }
    
    # Dossiers nécessitant une attention
    dossiers_urgents = dossiers_du_service.filter(
        Q(date_limite__lt=timezone.now().date() + timezone.timedelta(days=3)) &
        ~Q(statut__in=['TR', 'RJ'])
    )[:5]  # Les 5 plus urgents

    context = {
        'stats': stats,
        'dossiers_urgents': dossiers_urgents,
        'utilisateur': request.user
    }
    return render(request, 'dossiers/tableau_de_bord.html', context)
from .forms import DossierForm

@login_required
def ajouter_dossier(request):
    print("=== DEBUG AJOUTER DOSSIER ===")
    
    if request.method == 'POST':
        form = DossierForm(request.POST)
        print(f"Formulaire valide: {form.is_valid()}")
        
        if form.is_valid():
            print("Formulaire VALIDE - Sauvegarde...")
            dossier = form.save(commit=False)
            dossier.cree_par = request.user
            
            # GÉNÉRATION AUTOMATIQUE D'UN CODE UNIQUE - VERSION CORRIGÉE
            from datetime import datetime
            import random
            maintenant = datetime.now()
            
            # Crée un code vraiment unique avec timestamp + random
            timestamp = maintenant.strftime("%Y%m%d%H%M%S")
            random_str = str(random.randint(1000, 9999))  # 4 chiffres au lieu de 3
            dossier.code = f"DH-{timestamp}-{random_str}"
            
            print(f"Code généré: {dossier.code}")
            print(f"Code type: {type(dossier.code)}")
            print(f"Code valeur: {repr(dossier.code)}")
            
            try:
                dossier.save()
                print("Dossier SAUVEGARDÉ avec succès!")
                return redirect('liste_dossiers')
            except Exception as e:
                print(f"ERREUR lors de la sauvegarde: {e}")
                # Réafficher le formulaire avec erreur
    else:
        form = DossierForm()
    
    return render(request, 'dossiers/ajouter_dossier.html', {'form': form})
@login_required
def modifier_dossier(request, dossier_id):
    dossier = get_object_or_404(Dossier, id=dossier_id)
    
    # Vérification des permissions
    if not (request.user.is_staff or dossier.assigne_a == request.user):
        return redirect('liste_dossiers')
    
    if request.method == 'POST':
        form = DossierForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            return redirect('liste_dossiers')
    else:
        form = DossierForm(instance=dossier)
    
    return render(request, 'dossiers/modifier_dossier.html', {'form': form, 'dossier': dossier})
# À ajouter dans views.py
@login_required
def modifier_dossier(request, dossier_id):
    dossier = get_object_or_404(Dossier, id=dossier_id)
    # Vérifier les permissions...
    # Formulaire de modification...
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def modifier_dossier(request, dossier_id):
    """
    Modification d'un dossier existant avec vérification des permissions
    """
    print(f"=== DEBUG MODIFICATION DOSSIER {dossier_id} ===")
    
    # Récupère le dossier ou renvoie une 404
    dossier = get_object_or_404(Dossier, id=dossier_id)
    
    # VÉRIFICATION DES PERMISSIONS
    utilisateur = request.user
    peut_modifier = False
    
    if utilisateur.service and utilisateur.service.code == "DIR":
        peut_modifier = True  # La DIR peut tout modifier
        print("Permission: Super Admin")
    elif utilisateur.est_admin_service and dossier.assigne_a and dossier.assigne_a.service == utilisateur.service:
        peut_modifier = True  # Admin peut modifier les dossiers de son service
        print("Permission: Admin de service")
    elif dossier.assigne_a == utilisateur:
        peut_modifier = True  # Utilisateur peut modifier ses propres dossiers
        print("Permission: Propriétaire du dossier")
    
    if not peut_modifier:
        print("ACCÈS REFUSÉ - Redirection")
        return redirect('liste_dossiers')
    
    # TRAITEMENT DU FORMULAIRE
    if request.method == 'POST':
        form = DossierForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            print("Dossier MODIFIÉ avec succès!")
            return redirect('liste_dossiers')
        else:
            print("Formulaire invalide")
    else:
        form = DossierForm(instance=dossier)
    
    context = {
        'form': form,
        'dossier': dossier,
        'utilisateur': utilisateur
    }
    return render(request, 'dossiers/modifier_dossier.html', context)