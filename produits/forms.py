from django import forms
from .models import Produit, ImageProduit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'categorie']  
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'categorie': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ImageProduitForm(forms.ModelForm):
    class Meta:
        model = ImageProduit
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }