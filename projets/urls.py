from django.urls import path
from projets.views import AjouterEmployes, Assigner, ConnexionView, Enregistrement, LogTime, Mesprojets, ajouterProjet, ajouterSousProjet, dashboard, detailEmploye, detailProjet, employes, get_projets_par_employe, modifierEmploye, modifierProjet, projets, supprimeSousproj, supprimerEmploye, supprimerProjet

from django.contrib.auth import views as authentification_views

urlpatterns = [
    path('', projets, name="projets"),
    path('ajouterprojet/', ajouterProjet, name="ajouterProjet"),
    path('modifierprojet/<str:code>/', modifierProjet, name="modifierProjet"),
    path('detailprojet/<str:code>/', detailProjet, name="detailProjet"),
    path('supprimerprojet/<str:code>/', supprimerProjet, name="supprimerProjet"),
    path('assigner/<str:code>/', Assigner, name="AssignerEmployes"),
    
    path('employes/', employes, name="employes"),
    path('ajouteremploye/', AjouterEmployes, name="ajouterEmployes"),
    path('detailemploye/<str:code>/', detailEmploye, name="detailEmploye"),
    path('modifieremploye/<str:code>/', modifierEmploye, name="modifierEmploye"),
    path('supprimeremploye/<str:code>/', supprimerEmploye, name="supprimerEmploye"),
    path('ajouterssprojet/<str:code>', ajouterSousProjet, name="ajoutersp"),
    path('supprimerssproj/<str:code>/', supprimeSousproj, name="supprimerSp"),
    
    path('Logwork', LogTime, name="LogTime"),
    path('get_projets/', get_projets_par_employe, name='get_projets_par_employe'),
    
    path('dashboard/', dashboard, name="dashboard"),
    
    path('enregistrement/', Enregistrement, name='enregistrement'),
    path('login/', ConnexionView.as_view(), name='login'),
    path('logout/', authentification_views.LogoutView.as_view(template_name = 'usagers/logout.html'), name='logout'),
    
    path('mesprojets/', Mesprojets, name='mesprojets'),
]



