from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
timezone.now

# Modèle Admin
class Admin(models.Model):
    nom_admin = models.CharField(max_length=100)
    email_admin = models.EmailField(unique=True)
    login_admin = models.CharField(max_length=100, unique=True)
    password_admin = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_admin

# Modèle Client
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_client = models.CharField(max_length=100)
    email_client = models.EmailField(unique=True)
    login_client = models.CharField(max_length=100, unique=True)
    password_client = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255, null=True, blank=True)  # Ajout d'un champ adresse

    def __str__(self):
        return self.nom_client

# Formulaire de création d'utilisateur
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# Modèle Catégorie
class Categorie(models.Model):
    nom_categorie = models.CharField(max_length=100, unique=True)
    description_categorie = models.TextField(default="Description par défaut")


    def __str__(self):
        return self.nom_categorie

# Modèle Produit
class Produit(models.Model):
    nom_produit = models.CharField(max_length=255)
    description_produit = models.TextField(default="Description par défaut")
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)  # Ajoute ce champ
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    
    # Image produit en local, facultatif
    image_produit = models.ImageField(upload_to='produits/', null=True, blank=True)


    def __str__(self):
        return self.nom_produit

# Modèle Commande
class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(default=timezone.now)

    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('expédiée', 'Expédiée'),
        ('livrée', 'Livrée'),
        ('annulée', 'Annulée'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')

    def __str__(self):
        return f"Commande {self.id} - {self.client.nom_client}"


class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="produits")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom_produit} - Commande {self.commande.id}"

class HistoriqueCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)

    def __str__(self):
        return f"Historique - Commande {self.commande.id}"
