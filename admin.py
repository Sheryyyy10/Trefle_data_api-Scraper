from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Plant)
admin.site.register(Family)
admin.site.register(Genus)
admin.site.register(MainSpecies)
admin.site.register(Species)
admin.site.register(SubSpecies)
admin.site.register(Variety)
admin.site.register(MainSpecieImage)
admin.site.register(PlantImages)