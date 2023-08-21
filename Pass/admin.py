from django.contrib import admin
from.models import PerevalAdded, Climber


class PerevalAddedAdmin(admin.ModelAdmin):
    list_display = ('beautyTitle', 'title', 'other_titles',
                    'connect', 'author', 'coords',
                    'category', 'images', 'status')
class ClimberAdmin(admin.ModelAdmin):
    list_display = ('mail',
            'fam',
            'name',
            'otc',
            'phone',)

admin.site.register(PerevalAdded, PerevalAddedAdmin)
admin.site.register(Climber, ClimberAdmin)

# Register your models here.
