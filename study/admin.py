from django.contrib import admin

from . import models



class ConceptUserAdmin(admin.ModelAdmin):
    list_display = ('user', 
            'concept', 'level', 'created',)
    list_editable = ('level', )
    
admin.site.register(models.ConceptUser, ConceptUserAdmin)