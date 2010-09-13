from django.contrib import admin
from models import *

class NameTypeAdmin(admin.ModelAdmin):
    list_display = ('Type', 'Slug')

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

class GeneLocationAdmin(admin.ModelAdmin):
    list_display = ('Gene', 'Genome')

class ProductLocationAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Gene')

admin.site.register(Gene, GeneAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Name, NameAdmin)
admin.site.register(GeneLocation, GeneLocationAdmin)
admin.site.register(ProductLocation, ProductLocationAdmin)
