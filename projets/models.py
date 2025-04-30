from django.db import models

#Create your models here.

class Employe(models.Model):
    choix_statut = (('G', 'Gestionnaire'),
                    ('E', 'Employe'))
    codeEmploye = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    courriel = models.EmailField(null=True, unique=True)
    statut = models.CharField(max_length=1, choices=choix_statut)
    
    def __str__(self):
        return self.nom + ',' + self.prenom
   
    
class Projet(models.Model):
    codeProjet = models.CharField(max_length=10, primary_key=True)
    nomProjet = models.CharField(max_length=40)
    dateDebut = models.DateField(null=True)   
    dateEcheanche = models.DateField(null=True) 
    description = models.TextField(blank=True)
    employes = models.ManyToManyField(Employe, blank=True, related_name='projets')
    
    def __str__(self):
        return self.nomProjet
    

class SousProjet(models.Model):
    codeSousProjet = models.CharField(max_length=10, primary_key=True)
    nomSp = models.CharField(max_length=40)
    dateDebutSp = models.DateField(null=True)
    dateEcheanceSp = models.DateField(null=True)
    descriptionSp = models.TextField(blank=True)
    projet = models.ForeignKey(Projet, on_delete=models.DO_NOTHING, null=True, related_name='sous_projets')   
   
    def __str__(self):
        return self.nomSp
    

class WorkTime(models.Model):
    date_travail = models.DateField(null=True)
    heuresTravail = models.DecimalField(max_digits=4, decimal_places=2)
    commentaire = models.TextField(blank=True, null=True)
    date_saisie = models.DateTimeField(auto_now_add=True)
    employe = models.ForeignKey(Employe, on_delete=models.DO_NOTHING)
    projet = models.ForeignKey(Projet, on_delete=models.DO_NOTHING, null=True)
    sous_projet = models.ForeignKey(SousProjet, on_delete=models.DO_NOTHING, null=True)
