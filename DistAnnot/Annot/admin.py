from django.contrib import admin
from DistAnnot.Annot.models import *

class MutationAnnotAdmin(admin.ModelAdmin):
    pass


class InteractionEffectAnnotAdmin(admin.ModelAdmin):
    pass

class GeneAnnotAdmin(admin.ModelAdmin):
    pass

admin.site.register(MutationAnnot, MutationAnnotAdmin)
admin.site.register(InteractionEffectAnnot, InteractionEffectAnnotAdmin)
admin.site.register(GeneAnnot, GeneAnnotAdmin)
