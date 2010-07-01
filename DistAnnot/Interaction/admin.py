from django.contrib import admin
from DistAnnot.Interaction.models import *

class SentenceAdmin(admin.ModelAdmin):
    pass


class InteractionAdmin(admin.ModelAdmin):
    pass

class MutationAdmin(admin.ModelAdmin):
    pass

class InteractionEffectAdmin(admin.ModelAdmin):
    pass

class GeneAdmin(admin.ModelAdmin):
    pass

class InteractionTypeAdmin(admin.ModelAdmin):
    pass

class EffectTypeAdmin(admin.ModelAdmin):
    pass

class ArticleAdmin(admin.ModelAdmin):
    pass

class ExtraGeneNameAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Mutation, MutationAdmin)
admin.site.register(InteractionEffect, InteractionEffectAdmin)
admin.site.register(Gene, GeneAdmin)
admin.site.register(InteractionType, InteractionTypeAdmin)
admin.site.register(EffectType, EffectTypeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ExtraGeneName, ExtraGeneNameAdmin)

