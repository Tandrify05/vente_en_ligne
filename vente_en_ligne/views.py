from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # Pour gérer les utilisateurs
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Produit, Categorie, Commande, Client, CommandeProduit
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Client
from .forms import CustomUserCreationForm
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import json
timezone.now



def home(request):
    return render(request, "home/home.html")

@login_required  # Cela permet de s'assurer que l'utilisateur est connecté
def menu(request):
    return render(request, "user/menu.html") 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        contact = request.POST.get('contact')  # Récupère le contact
        adresse = request.POST.get('adresse')  # Récupère l'adresse

        if form.is_valid():
            print("✅ Formulaire valide")
            print("📌 Champs disponibles :", form.cleaned_data.keys())  # Debugging

            # Création de l'utilisateur
            user = form.save()

            # Création du client
            Client.objects.create(
                user=user,
                nom_client=user.username,
                email_client=user.email,
                login_client=user.username,
                password_client=user.password,  # Django gère déjà le hash du mot de passe
                contact=contact,
                adresse=adresse
            )

            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect('login')
        else:
            messages.error(request, "Le formulaire est invalide. Veuillez vérifier les champs.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'home/register.html', {'form': form})





def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Vérifier si l'utilisateur est un admin ou un client
            if user.is_superuser:  # Vérification si l'utilisateur est un admin
                messages.success(request, "Connexion réussie ! Bienvenue, Admin.")
                return redirect("admin_home")  # Redirige vers la page d'administration
            else:
                messages.success(request, "Connexion réussie ! Bienvenue, Client.")
                return redirect("menu")  # Redirige vers la page d'accueil du client
        else:
            messages.error(request, "Identifiants incorrects. Réessaie.")
    
    return render(request, "home/login.html")  # Page de connexion


# Déconnexion
def logout_view(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect("login")  # Redirige vers la connexion après la déconnexion

def produits(request):
    produits_list = Produit.objects.all()  # Récupère tous les produits
    return render(request, 'user/produits_list.html', {'produits': produits_list})


@login_required
def mes_commandes(request):
    try:
        client = Client.objects.get(user=request.user)  # 🔥 Récupérer le Client lié au User
        commandes = Commande.objects.filter(client=client).order_by('-date_commande')
    except Client.DoesNotExist:
        commandes = []  # Si le client n'existe pas, éviter l'erreur

    return render(request, 'user/commandes_list.html', {'commandes': commandes})

@login_required
def modifier_commande(request, commande_id):
    # Récupérer la commande et ses produits associés
    commande = get_object_or_404(Commande, id=commande_id)

    # Si la requête est en méthode POST, nous mettons à jour les données
    if request.method == 'POST':
        statut = request.POST.get('status')
        commande.status = statut
        commande.save()

        # Mettre à jour les quantités des produits associés à la commande
        for commande_produit in commande.produits.all():
            quantite_key = f'quantite_{commande_produit.id}'
            quantite = request.POST.get(quantite_key)
            if quantite:
                commande_produit.quantite = int(quantite)
                commande_produit.save()

        print(commande.produits.all())  # Débogage pour vérifier que les produits sont bien associés


        # Rediriger vers la page des commandes une fois les modifications effectuées
        return redirect('mes_commandes')

    # Si la méthode est GET, on affiche la page de modification
    return render(request, 'user/modifier_commande.html', {'commande': commande})



def supprimer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    if request.method == 'POST':
        commande.delete()
        return redirect('mes_commandes')  # Redirige vers la page des commandes

    return render(request, 'utilisateur/confirmer_supprimer.html', {'commande': commande})

@login_required
def mon_compte(request):
    try:
        # Accède aux informations du client associé à l'utilisateur connecté
        client = request.user.client
    except Client.DoesNotExist:
        # Si le client n'existe pas, redirige l'utilisateur vers une page pour compléter son profil
        client = None

    # Si le client existe, on peut afficher ses informations
    if client:
        print(client.nom_client, client.email_client, client.contact, client.adresse)  # Vérification dans la console

    # Passe les données du client au template
    return render(request, 'user/mon_compte.html', {'client': client})
@login_required

@login_required
def modifier_compte(request):
    client = request.user.client

    if request.method == 'POST':
        # Mettre à jour les informations personnelles
        client.nom_client = request.POST.get('nom_client')
        client.email_client = request.POST.get('email_client')
        client.contact = request.POST.get('contact')
        client.adresse = request.POST.get('adresse')
        client.save()

        # Vérifier si l'utilisateur souhaite changer son mot de passe
        if 'current_password' in request.POST and request.POST['current_password']:
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            # Valider le mot de passe
            if new_password == confirm_password:
                user = request.user
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Met à jour la session de l'utilisateur
                    messages.success(request, "Votre mot de passe a été modifié avec succès.")
                else:
                    messages.error(request, "Le mot de passe actuel est incorrect.")
            else:
                messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
        
        return redirect('mon_compte')

    return render(request, 'user/modifier_compte.html')

def details_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    return render(request, 'user/details_produit.html', {'produit': produit})

@csrf_exempt
def commander_produit(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            produit_id = data.get("produit_id")
            quantite = data.get("quantite")
            client = request.user.client  # Supposant que l'utilisateur est connecté et lié à un client

            if not produit_id or not quantite:
                return JsonResponse({"success": False, "message": "Données invalides."}, status=400)

            produit = Produit.objects.get(id=produit_id)
            prix_total = produit.prix * int(quantite)

            # Créer la commande
            commande = Commande.objects.create(client=client, prix_total=prix_total)
            CommandeProduit.objects.create(commande=commande, produit=produit, quantite=int(quantite))

            return JsonResponse({"success": True, "message": "Commande enregistrée avec succès !"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    else:
        return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)