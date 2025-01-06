from django.contrib import admin
from django.urls import path
from produits import views  # Import correct des vues depuis l'application "produits"
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Catégories de produits
    path('bagues/', views.liste_bagues, name='liste_bagues'),  # Vue: liste_bagues
    path('bracelets/', views.liste_bracelets, name='liste_bracelets'),  # Vue: liste_bracelets
    path('bouclesoreilles/', views.liste_bouclesoreilles, name='liste_bouclesoreilles'),  # Vue: liste_bouclesoreilles
    path('cartesdiv/', views.liste_cartesdiv, name='liste_cartesdiv'),  # Vue: liste_cartesdiv
    path('colliers/', views.liste_colliers, name='liste_colliers'),  # Vue: liste_colliers
    path('chapelets/', views.liste_chapelets, name='liste_chapelets'),  # Vue: liste_chapelets
    path('bijouxcheville/', views.liste_bijouxcheville, name='liste_bijouxcheville'),  # Vue: liste_bijouxcheville
    path('malas/', views.liste_malas, name='liste_malas'),  # Vue: liste_malas
    path('parures/', views.liste_parures, name='liste_parures'),  # Vue: liste_parures
    path('pendules/', views.liste_pendules, name='liste_pendules'),  # Vue: liste_pendules
    path('portecles/', views.liste_portecles, name='liste_portecles'),  # Vue: liste_portecles

    # Pages générales
    path('apropos/', views.apropos, name='apropos'),  # Vue: apropos
    path('contact/', views.contact, name='contact'),  # Vue: contact
    
    # Gestion des produits
    path('ajouter-produit/', views.ajouter_produit, name='ajouter_produit'),  # Vue: ajouter_produit
    path('produit/<int:produit_id>/', views.produit_detail, name='produit_detail'),  # Vue: produit_detail
    path('modifier-produit/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),  # Vue: modifier_produit
    path('supprimer-produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),  # Vue: supprimer_produit

    # Gestion du panier
    path('panier/', views.panier, name='panier'),  # Vue: panier
    path('retirer-du-panier/<int:produit_id>/', views.retirer_du_panier, name='retirer_du_panier'),  # Vue: retirer_du_panier
    path('mettre-a-jour-panier/<int:produit_id>/', views.mettre_a_jour_panier, name='mettre_a_jour_panier'),  # Vue: mettre_a_jour_panier

    # Gestion du paiement
    path('paiement/', views.passer_au_paiement, name='passer_au_paiement'),  # Vue: passer_au_paiement
    path('traitement-paiement/', views.traitement_paiement, name='traitement_paiement'),  # Vue: traitement_paiement

    # Test d'envoi d'e-mail
    path('test-email/', views.test_envoi_email, name='test_email'),  # Vue: test_envoi_email
    # Gestion du panier
    path('retirer-du-panier/<int:produit_id>/', views.retirer_du_panier, name='retirer_du_panier'),
    path('mettre-a-jour-panier/<int:produit_id>/', views.mettre_a_jour_panier, name='mettre_a_jour_panier'),

    # Gestion des produits
    path('supprimer-produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
]

# Serve static and media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
