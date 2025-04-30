from django.shortcuts import render
from django.http import HttpResponse

# Section des vues

def accueil(request):
    return render(request, "accueil.html")

    
def apropos(request):
    contexte = {
        'environnement' : {'python' : "3.13.1", 'django' : "5.1.5", 'vs_code' : "1.97.1", 'bootstrap' : "5.3.3"},
        'concepteur' : {'nom' : "Marechal Damas Nobousse", 'noEtudiant' : "202332555", 'cours' : "Projet d'Intégration Web", 'travail' : "Gestion de projets(Application Web 1)", 'dateRemise' : "06 avril 2025", 'cegep' : "Cégep de La Pocatière, département de l'Informatique"}
    }
    
    return render(request, "apropos.html", contexte)


def documentation(request):
    return render(request, "documentation.html") 
         