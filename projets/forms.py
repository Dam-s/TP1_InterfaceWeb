from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from projets.models import Employe, Projet, SousProjet, WorkTime

class AjoutProjetForm(forms.ModelForm):
    class Meta:
        model =Projet
        exclude = ["Employe"]
        widgets = {
            'codeProjet':forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Code du projet'}),
            'nomProjet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du projet'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description du projet'}),
            'dateDebut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dateEcheanche': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ModifierProjetForm(forms.ModelForm):
    class Meta:
        model =Projet
        exclude = ["Employe", "codeProjet"]
        widgets = {
            'nomProjet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du projet'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description du projet'}),
            'dateDebut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dateEcheanche': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


# Formulaire pour l'assignation des employés
class AssignEmployeForm(forms.Form):
    employes = forms.ModelMultipleChoiceField(
        queryset=Employe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Permet d'envoyer un formulaire vide sans supprimer tous les employés
    )
    
#Formulaire d'ajout d'un employé 
class AjoutEmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = "__all__" 
        widgets = {
            'codeEmploye': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Code employé'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'courriel': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Courriel'}),
            'statut': forms.Select(attrs={'class' : 'form-control', 'value' : 'Selectionnez un statut'})
        }  

#Formulaire de modification d'un employé
class ModifierEmployeForm(forms.ModelForm):
     class Meta:
        model = Employe
        exclude = ["codeEmploye"] 
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'courriel': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Courriel'}),
            'statut': forms.Select(attrs={'class' : 'form-select'})
        }


class SousProjetForm(forms.ModelForm):
    class Meta:
        model = SousProjet
        exclude = ['projet'] 
        widgets = {
            'codeSousProjet':forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Code du sous projet'}),
            'nomSp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du sous-projet'}),
            'descriptionSp': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description du sous-projet'}),
            'dateDebutSp': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dateEcheanceSp': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


#Formualaire de log Work
class WorkTimeForm(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = ['date_travail', 'employe', 'projet', 'heuresTravail', 'commentaire']
        widgets = {
            'date_travail': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employe' : forms.Select(attrs={'class' : 'form-select'}),
            'projet': forms.Select(attrs={'class': 'form-select'}),
            'heuresTravail': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.25, 'min': 0}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

#Formulaire d'enregistrement
class EnregistrementForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'nom utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'prenom@outlook.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'mot de passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Saisissez le même mot de passe que précédemment'}),
        }

#Formulaire de connexion 
class ConnexionEmployeForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d’utilisateur',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )         