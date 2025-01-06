from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Produit, ImageProduit
from .forms import ProduitForm, ImageProduitForm
from django.contrib import messages
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def home(request):
    return render(request, 'index.html')

# Gestion des différentes listes de produits
def liste_bagues(request):
    produits = Produit.objects.filter(categorie="bagues").prefetch_related('images')
    return render(request, 'produits/page-bagues.html', {'produits': produits})

def liste_bracelets(request):
    produits = Produit.objects.filter(categorie="bracelets")
    return render(request, 'produits/page-bracelets.html', {'produits': produits})

def liste_bouclesoreilles(request):
    produits = Produit.objects.filter(categorie="boucles oreilles")
    return render(request, 'produits/page-bouclesoreilles.html', {'produits': produits})

def liste_cartesdiv(request):
    produits = Produit.objects.filter(categorie="cartes divinatoires")
    return render(request, 'produits/page-cartesdiv.html', {'produits': produits})

def liste_colliers(request):
    produits = Produit.objects.filter(categorie="colliers")
    return render(request, 'produits/page-colliers.html', {'produits': produits})

def liste_chapelets(request):
    produits = Produit.objects.filter(categorie="chapelets")
    return render(request, 'produits/page-chapelet.html', {'produits': produits})

def liste_bijouxcheville(request):
    produits = Produit.objects.filter(categorie="bijouxcheville")
    return render(request, 'produits/page-bijouxcheville.html', {'produits': produits})

def liste_malas(request):
    produits = Produit.objects.filter(categorie="malas")
    return render(request, 'produits/page-malas.html', {'produits': produits})

def liste_parures(request):
    produits = Produit.objects.filter(categorie="parures")
    return render(request, 'produits/page-parures.html', {'produits': produits})

def liste_pendules(request):
    produits = Produit.objects.filter(categorie="pendules")
    return render(request, 'produits/page-pendulediv.html', {'produits': produits})

def liste_portecles(request):
    produits = Produit.objects.filter(categorie="portecles")
    return render(request, 'produits/page-portecles.html', {'produits': produits})

def contact(request):
    return render(request, 'contact.html')

def apropos(request):
    return render(request, 'apropos.html')

# Vue pour ajouter un produit (formulaire)
def ajouter_produit(request):
    ImageProduitFormSet = modelformset_factory(ImageProduit, form=ImageProduitForm, extra=4)

    if request.method == "POST":
        produit_form = ProduitForm(request.POST, request.FILES)
        formset = ImageProduitFormSet(request.POST, request.FILES, queryset=ImageProduit.objects.none())

        if produit_form.is_valid() and formset.is_valid():
            produit = produit_form.save()  # Sauvegarde du produit

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = ImageProduit(produit=produit, image=image)
                    photo.save()
            messages.success(request, "Produit ajouté avec succès !")
            return redirect('ajouter_produit')  # Redirection après l'ajout du produit
    else:
        produit_form = ProduitForm()
        formset = ImageProduitFormSet(queryset=ImageProduit.objects.none())

    # Récupérer tous les produits pour le tableau
    produits = Produit.objects.all()    

    return render(request, 'gestion/ajouter_produit.html', {
        'produit_form': produit_form,
        'formset': formset,
        'produits': produits,
    })

# Fonction pour gérer l'ajout au panier et la gestion des quantités
def produit_detail(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    images = produit.images.all()

    if request.method == "POST":
        quantite = int(request.POST.get('quantity', 1))
        panier = request.session.get('panier', {})

        if str(produit_id) in panier:
            panier[str(produit_id)] += quantite
        else:
            panier[str(produit_id)] = quantite

        request.session['panier'] = panier
        messages.success(request, "Produit ajouté au panier avec succès !")
        return redirect('panier')

    return render(request, 'produits/produit_detail.html', {'produit': produit, 'images': images})

# Fonction pour afficher le panier
def panier(request):
    panier = request.session.get('panier', {})
    produits = Produit.objects.filter(id__in=panier.keys())

    total_panier = 0
    for produit in produits:
        produit.quantite = panier[str(produit.id)]
        produit.sous_total = produit.prix * produit.quantite
        total_panier += produit.sous_total

    return render(request, 'commandes/panier.html', {'produits': produits, 'total_panier': total_panier})

# Vue pour modifier un produit
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == "POST":
        produit_form = ProduitForm(request.POST, instance=produit)
        if produit_form.is_valid():
            produit_form.save()
            messages.success(request, "Produit modifié avec succès !")
            return redirect('ajouter_produit')
    else:
        produit_form = ProduitForm(instance=produit)

    return render(request, 'gestion/modifier_produit.html', {'produit_form': produit_form})

# Vue pour supprimer un produit
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    produit.delete()
    messages.success(request, "Produit supprimé avec succès !")
    return redirect('ajouter_produit')

def retirer_du_panier(request, produit_id):
    panier = request.session.get('panier', {})

    if str(produit_id) in panier:
        del panier[str(produit_id)]  # Retirer le produit du panier

    request.session['panier'] = panier  # Mettre à jour la session
    return redirect('panier')  # Redirection vers le panier

def mettre_a_jour_panier(request, produit_id):
    if request.method == "POST":
        panier = request.session.get('panier', {})
        nouvelle_quantite = int(request.POST.get('quantite', 1))

        if str(produit_id) in panier:
            panier[str(produit_id)] = nouvelle_quantite  # Mettre à jour la quantité

        request.session['panier'] = panier  # Mettre à jour le panier dans la session
        return redirect('panier')  # Rediriger vers la page panier


def traitement_paiement(request):
    # Récupérer le panier de la session
    panier = request.session.get('panier', {})
    
    if not panier:
        return HttpResponse("Votre panier est vide.")
    
    # Récupérer les produits dans le panier
    produits = Produit.objects.filter(id__in=panier.keys())
    
    # Calcul du total à payer
    total = Decimal(0)
    for produit in produits:
        quantite = panier[str(produit.id)]
        total += produit.prix * quantite
    
    # Exemple d'intégration d'une API de paiement (c'est ici qu'on pourrait utiliser SumUp, Stripe, etc.)
    # Cela pourrait être une requête API vers un service externe pour traiter le paiement.
    # Pour cet exemple, on suppose que le paiement est réussi.
    
    # Enregistrement de la commande
    client = Client.objects.get(id=request.user.id)  # Supposons que l'utilisateur est un Client
    nouvelle_commande = Commande.objects.create(
        client=client,
        total=total,
        statut='Confirmée'  # Statut par défaut de la commande
    )
    
    # Ajouter les produits à la commande
    for produit in produits:
        nouvelle_commande.produits.add(produit)
    
    nouvelle_commande.save()  # Sauvegarder la commande
    
    # Vider le panier après le paiement réussi
    request.session['panier'] = {}
    
    # Confirmation du paiement
    return HttpResponse("Le paiement a été traité avec succès.")

# Gestion de la commande
def passer_au_paiement(request):
    panier = request.session.get('panier', {})
    produits = Produit.objects.filter(id__in=panier.keys())

    sous_total = sum(produit.prix * panier[str(produit.id)] for produit in produits)
    frais_livraison = Decimal('2.50')

    if sous_total >= 50:
        frais_livraison = Decimal('0.00')

    total = sous_total + frais_livraison

    # Envoi de l'e-mail de confirmation au client
    subject = 'Confirmation de votre commande'
    html_message = render_to_string('emails/confirmation_commande.html', {'commande': {'produits': produits, 'total': total}})
    plain_message = strip_tags(html_message)
    client_email = 'email_client@example.com'

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [client_email],
        html_message=html_message,
    )

    # Envoi d'un e-mail à la créatrice
    send_mail(
        'Nouvelle commande reçue',
        f'Une nouvelle commande a été passée avec un total de {total} €.',
        settings.DEFAULT_FROM_EMAIL,
        ['email_creatrice@example.com'],
    )

    return render(request, 'commandes/paiement.html', {
        'produits': produits,
        'sous_total': sous_total,
        'frais_livraison': frais_livraison,
        'total': total,
    })

# Fonction pour gérer le traitement de commande et envoyer un email de mise à jour
def traiter_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.statut = "Traitée"
    commande.save()

    subject = 'Commande traitée'
    html_message = render_to_string('emails/traitement_commande.html', {'commande': commande})
    plain_message = strip_tags(html_message)
    client_email = commande.client.email

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [client_email],
        html_message=html_message,
    )

    messages.success(request, "La commande a été traitée et un email a été envoyé au client.")
    return redirect('admin_commande_list')

# Fonction pour gérer l'expédition de commande
def expedier_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.statut = "Expédiée"
    commande.save()

    subject = 'Votre commande a été expédiée'
    html_message = render_to_string('emails/expedition_commande.html', {'commande': commande})
    plain_message = strip_tags(html_message)
    client_email = commande.client.email

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [client_email],
        html_message=html_message,
    )

    messages.success(request, "La commande a été expédiée et un email a été envoyé au client.")
    return redirect('admin_commande_list')

# Test d'envoi d'e-mail
def test_envoi_email(request):
    send_mail(
        'Test d\'envoi d\'email',
        'Voici un email de test pour vérifier la configuration d\'envoi d\'emails.',
        settings.DEFAULT_FROM_EMAIL,
        ['neghadly@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("L'email de test a été envoyé avec succès.")
