from django import forms
from .models import Dossier

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = [
            
            'denomination_commerciale',
            'fabricant', 
            'pays_origine',
            'type_demande',
            'date_depot',
            'date_limite',
            'evaluateur',
            'verificateur',
            'reserves',
            'certificat_ce'
        ]
        widgets = {
            'date_depot': forms.DateInput(attrs={'type': 'date'}),
            'date_limite': forms.DateInput(attrs={'type': 'date'}),
            'reserves': forms.Textarea(attrs={'rows': 3}),
        }