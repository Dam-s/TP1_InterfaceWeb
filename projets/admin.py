from django.contrib import admin

from projets.models import Employe, Projet, SousProjet, WorkTime

# Register your models here.
admin.site.register(Projet)
admin.site.register(SousProjet)
admin.site.register(Employe)
admin.site.register(WorkTime)