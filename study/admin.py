from django.contrib import admin

from . import models



class ConceptUserAdmin(admin.ModelAdmin):
    list_display = ('user', 
            'concept', 'level', 'created',)
    list_editable = ('level', )
    
admin.site.register(models.ConceptUser, ConceptUserAdmin)

class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('created', 
            'user', 'badge_name', 'user_alerted',)
    list_editable = ('user_alerted', )
    
admin.site.register(models.UserBadge, UserBadgeAdmin)