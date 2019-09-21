from django.contrib import admin

from . import models



class ConceptUserAdmin(admin.ModelAdmin):
    list_display = ('user', 
            'concept', 'level', 'created',)
    
admin.site.register(models.ConceptUser, ConceptUserAdmin)