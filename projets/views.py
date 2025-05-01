from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from projets.forms import AjoutEmployeForm, AjoutProjetForm, AssignEmployeForm, ConnexionEmployeForm, EnregistrementForm, ModifierEmployeForm, ModifierProjetForm, SousProjetForm, WorkTimeForm, WorkTimeFormEmploye
from projets.models import Employe, Projet, SousProjet, WorkTime

# Create your views here.
def projets(request):
    mesProjets = Projet.objects.all()
    return render(request, "projets.html", context={'mesProjets' : mesProjets}) 

def ajouterProjet(request):
    if request.method == 'POST':
        form = AjoutProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.save()
        return redirect("/projets")   
    else:
        form = AjoutProjetForm()
    return render(request, "ajoutProjet.html", context={'form' : form})         

def modifierProjet(request, code):
    ProjetAModifier = Projet.objects.get(codeProjet = code)
    if request.method == 'POST':
        form = ModifierProjetForm(request.POST, instance=ProjetAModifier)
        if form.is_valid():
            form.save() 
        return redirect('accueil')
    else:
        form = ModifierProjetForm(instance=ProjetAModifier)
    return render(request, "modifierProjet.html", context={'form': form, 'leProjetMod' : ProjetAModifier})

# def detailProjet(request, code):
#     leProjet = Projet.objects.get(codeProjet = code)
#     return render(request, "detailProjet.html", context={'leProjet' : leProjet})

def supprimerProjet(request, code):
    ProjetASupp = Projet.objects.get(codeProjet = code)
    if request.method == 'POST':
        ProjetASupp.delete()
        return redirect('/projets')
    return render(request, 'DelProjet.html', context={'leProjetSupp' : ProjetASupp})


def Assigner(request, code):
    projet = get_object_or_404(Projet, codeProjet= code)

    if request.method == 'POST':
        form = AssignEmployeForm(request.POST)
        if form.is_valid():
            nouveaux_employes = form.cleaned_data['employes']
            
            # Ajouter les nouveaux employés sélectionnés
            for employe in nouveaux_employes:
                projet.employes.add(employe)

            # Supprimer les employés qui ne sont plus sélectionnés
            for employe in projet.employes.all():
                if employe not in nouveaux_employes:
                    projet.employes.remove(employe)

            return redirect('/projets')
    else:
        form = AssignEmployeForm(initial={'employes': projet.employes.all()})

    return render(request, 'assignerEmp.html', {'form': form, 'projet': projet})


def employes(request):
    mesEmployes = Employe.objects.all()
    return render(request, 'employes.html', context={'mesEmployes' : mesEmployes})

def AjouterEmployes(request):
    if request.method == 'POST':
        form = AjoutEmployeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("employes")   
    else:
        form = AjoutEmployeForm()
    return render(request, "ajouterEmploye.html", context={'form' : form})   

def detailEmploye(request, code):
    monEmploye = Employe.objects.get(codeEmploye = code)
    return render(request, "detailEmploye.html", context={'monEmploye' : monEmploye})

def modifierEmploye(request, code):
    EmployeAModifier = Employe.objects.get(codeEmploye = code)
    if request.method == 'POST':
        form = ModifierEmployeForm(request.POST, instance=EmployeAModifier)
        if form.is_valid():
            form.save() 
        return redirect('employes')
    else:
        form = ModifierEmployeForm(instance=EmployeAModifier)
    return render(request, "modifierEmploye.html", context={'form': form, 'lemployeMod' : EmployeAModifier})

def supprimerEmploye(request, code):
    EmployeASupp = Employe.objects.get(codeEmploye = code)
    if request.method == 'POST':
        EmployeASupp.delete()
        return redirect('employes')
    return render(request, 'suppEmploye.html', context={'lempSupp' : EmployeASupp})


def ajouterSousProjet(request, code):
    projet = get_object_or_404(Projet, codeProjet=code)

    if request.method == 'POST':
        form = SousProjetForm(request.POST)
        if form.is_valid():
            sousprojet = form.save(commit=False)
            sousprojet.projet = projet
            sousprojet.save()
            return redirect('/projets')
    else:
        form = SousProjetForm()

    return render(request, 'ajouterSsproj.html', {'form': form, 'projet': projet})

def supprimeSousproj(request, code):
    sp = get_object_or_404(SousProjet, codeSousProjet=code)
    if request.method == 'POST':
       sp.delete()
       return redirect('accueil')



def LogTime(request):
    if request.method == 'POST':
        form = WorkTimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')  # ou autre vue de confirmation
    else:
        form = WorkTimeForm()

    employes = Employe.objects.all()
    print(form)
    return render(request, 'logWork.html', {'form': form, 'employes': employes})


# Retourner les projets d'un employé donné en JSON
def get_projets_par_employe(request):
    employe_id = request.GET.get('employe_id')
    projets = []

    if employe_id:
        try:
            employe = Employe.objects.get(pk=employe_id)
            projets = employe.projets.all()
        except Employe.DoesNotExist:
            pass

    data = [{'id': projet.codeProjet, 'nom': projet.nomProjet} for projet in projets]
    return JsonResponse(data, safe=False)


def dashboard(request):
    projets = Projet.objects.all()
    employes = Employe.objects.all()
    worktimes = WorkTime.objects.all()

    projet_filtre = request.GET.get('projet')
    employe_filtre = request.GET.get('employe')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    # Filtrage selon les champs du formulaire
    if projet_filtre:
        worktimes = worktimes.filter(projet__codeProjet=projet_filtre)

    if employe_filtre:
        worktimes = worktimes.filter(employe__codeEmploye=employe_filtre)

    if date_debut:
        worktimes = worktimes.filter(date_travail__gte=date_debut)

    if date_fin:
        worktimes = worktimes.filter(date_travail__lte=date_fin)

    # Agrégation des heures par employé
    grouped_data = worktimes.values('employe__nom', 'employe__prenom').annotate(
        total_heures=Sum('heuresTravail')
    )

    labels = [f"{entry['employe__prenom']} {entry['employe__nom']}" for entry in grouped_data]
    data = [float(entry['total_heures']) for entry in grouped_data]

    return render(request, 'dashboard.html', {
        'projets': projets,
        'employes': employes,
        'worktimes': worktimes,
        'labels': labels,
        'data': data,
    })



def detailProjet(request, code):
    projet = Projet.objects.get(codeProjet=code)
    
    # Calculer le total des heures travaillées sur le projet
    heures_travaillees = WorkTime.objects.filter(projet=projet).aggregate(Sum('heuresTravail'))['heuresTravail__sum'] or 0
    
    # Calculer le nombre de jours entre dateDebut et dateEcheance et le multiplier par 24 pour obtenir les heures totales
    date_debut = projet.dateDebut
    date_echeance = projet.dateEcheanche
    delta = date_echeance - date_debut
    heures_totales = delta.days * 24
    
    # Calculer le pourcentage du travail effectué
    if heures_totales > 0:
        pourcentage = (heures_travaillees / heures_totales) * 100
    else:
        pourcentage = 0
    
    return render(request, 'detailProjet.html', {
        'leProjet': projet,
        'heures_travaillees': heures_travaillees,
        'heures_totales': heures_totales,
        'pourcentage': pourcentage,
    })


# View d'enregistrement
def Enregistrement(request):
    if request.method == "POST":
        form = EnregistrementForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bonjour {username}, vous êtes enregistré !')
            return redirect('accueil')
    else:
        form = EnregistrementForm() 
    return render (request, 'usagers/enregistrement.html', {'form' : form})

#View de connexion
class ConnexionView(LoginView):
    template_name = "usagers/login.html"
    authentication_form = ConnexionEmployeForm


@login_required
def Mesprojets(request):
    email_utilisateur = request.user.email
    employe = get_object_or_404(Employe, courriel=email_utilisateur)

    projets = Projet.objects.filter(employes=employe)

    projets_info = []
    for projet in projets:
        est_gestionnaire = employe.statut == 'G'
        projets_info.append({'projet': projet, 'est_gestionnaire': est_gestionnaire})

    return render(request, 'usagers/mesprojets.html', {'projets_info': projets_info})

@login_required
def LogTimeEmploye(request):
    employe = Employe.objects.get(courriel=request.user.email)

    if request.method == 'POST':
        form = WorkTimeFormEmploye(request.POST, employe=employe)
        if form.is_valid():
            work = form.save(commit=False)
            work.employe = employe
            work.save()
            return redirect('mesprojets')
    else:
        form = WorkTimeFormEmploye(employe=employe)

    return render(request, 'usagers/logworkEmploye.html', {'form': form})
