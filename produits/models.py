from django.db import models

class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50)
    quantite = models.IntegerField(default=1)  # Ajout d'une valeur par défaut

    def __str__(self):
        return self.nom

class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='produits/')

    def __str__(self):
        return f"Image for {self.produit.nom}"

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()

class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=50, choices=[('Confirmée', 'Confirmée'), ('Traitée', 'Traitée'), ('Expédiée', 'Expédiée')])

    def __str__(self):
        return f"Commande de {self.client.nom} - {self.statut}"
