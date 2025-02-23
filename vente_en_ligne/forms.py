from django import forms
from .models import Produit
from django.contrib.auth.forms import UserCreationForm  # ✅ Import correct
from django.contrib.auth.models import User

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom_produit', 'description_produit', 'prix', 'stock_quantity', 'categorie', 'image_url']

# ✅ Utiliser UserCreationForm de Django
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    contact = forms.CharField(max_length=15, required=True, label="Numéro de téléphone")
    adresse = forms.CharField(max_length=255, required=True, label="Adresse")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email
