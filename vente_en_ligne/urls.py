from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),  
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('menu/', views.menu, name='menu'),  # Page d'accueil après connexion
    path('produits/', views.produits, name='produits'),  # Liste des produits
    path('mes_commandes/', views.mes_commandes, name='mes_commandes'),
    path('commandes/', views.mes_commandes, name='mes_commandes'),  # Mes commandes
    path('commande/modifier/<int:commande_id>/', views.modifier_commande, name='modifier_commande'),
    path('commande/supprimer/<int:commande_id>/', views.supprimer_commande, name='supprimer_commande'),
    path('compte/', views.mon_compte, name='mon_compte'),  # Infos sur mon compte
    path('modifier-compte/', views.modifier_compte, name='modifier_compte'),
    path('produit/<int:produit_id>/', views.details_produit, name='details_produit'),
    path("commander/", views.commander_produit, name="commander_produit"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)