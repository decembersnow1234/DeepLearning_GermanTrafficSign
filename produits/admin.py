from django.contrib import admin
from .models import Produit, ImageProduit, Client, Commande  # Ajoute l'import de 'Commande'

# Inline pour ajouter plusieurs images à un produit
class ImageProduitInline(admin.TabularInline):
    model = ImageProduit
    extra = 4  # Nombre de champs supplémentaires pour ajouter des images

# Configuration de l'affichage des produits dans l'admin
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix')  # Afficher ces colonnes dans la liste des produits
    list_filter = ('categorie',)  # Filtre pour faciliter la gestion des produits par catégorie
    search_fields = ('nom', 'categorie')  # Permettre la recherche par nom et catégorie
    inlines = [ImageProduitInline]  # Associer les images à chaque produit

# Enregistrer le modèle avec la configuration dans l'admin
admin.site.register(Produit, ProduitAdmin)
admin.site.register(ImageProduit)
admin.site.register(Client)
admin.site.register(Commande)  # Enregistrement du modèle 'Commande'
