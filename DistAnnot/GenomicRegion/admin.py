from django.contrib import admin
from models import *

class NameTypeAdmin(admin.ModelAdmin):
    pass

class OrganismAdmin(admin.ModelAdmin):
    pass

class GenomeAdmin(admin.ModelAdmin):
    pass

admin.site.register(NameType, NameTypeAdmin)
admin.site.register(Organism, OrganismAdmin)
admin.site.register(Genome, GenomeAdmin)

#only for debugging purposes!!!

class GeneAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

class NameAdmin(admin.ModelAdmin):
    pass

admin.site.register(Gene, GeneAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Name, NameAdmin)
