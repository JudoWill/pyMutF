from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


# Create your models here.


#Abstract Models

class NameMixin(models.Model):
    SymbolOrder = ('gene-id',
                   'refseq',
                   'offical-full-name',
                   'official-symbol',
                   'tax-id')
    NameOrder = ('offical-full-name',
                 'official-symbol',
                 'synonym')


    Names = models.ManyToManyField('Name')

    class Meta:
        abstract = True

    def get_official_symbol(self):
        return self.get_name(self.SymbolOrder)

    def get_official_name(self):
        return self.get_name(self.NameOrder)


    def get_name(self, name_order):

        for field in name_order:
            try:
                return self.Names.get(NameType__Slug__exact = field)
            except ObjectDoesNotExist:
                pass
            except MultipleObjectsReturned:
                return self.Names.filter(NameType__Slug__exact = field)[0]

        return self.Names.all()[0]



    def __unicode__(self):
        return self.get_official_symbol().Name
        
class ProductMixin(models.Model):
    pass
    
    class Meta:
        abstract = True

class LocationMixin(models.Model):
    Start = models.IntegerField()
    Stop = models.IntegerField()

    class Meta:
        abstract = True

#Name Models

class Name(models.Model):
    Name = models.CharField(max_length = 255)
    NameType = models.ForeignKey('NameType')

    def __unicode__(self):
        return self.Name

class NameType(models.Model):
    Type = models.CharField(max_length = 255)
    Slug = models.SlugField(max_length = 255)


    def __unicode__(self):
        return self.Type

#Organism Related models

class Organism(NameMixin):
    SymbolOrder = ('offical-full-name',
                   'refseq',
                   'official-symbol',
                   'tax-id')

    def get_absolute_url(self):
        return reverse('organism_object_detail', kwargs = {'object_id':self.pk})

class Genome(NameMixin):
    SymbolOrder = ('refseq',
                   'offical-full-name',
                   'official-symbol',
                   'tax-id')
    Organism = models.ForeignKey(Organism)

    def get_absolute_url(self):
        return reverse('genome_object_detail', kwargs = {'object_id':self.pk})
#Gene/Product related Models

class Gene(NameMixin, ProductMixin):
    Genome = models.ManyToManyField(Genome, through = 'GeneLocation')

    def get_absolute_url(self):
        return reverse('gene_object_detail', kwargs = {'object_id':self.pk})

class Product(NameMixin):
    Gene = models.ManyToManyField(Gene, through = 'ProductLocation')

    def get_absolute_url(self):
        return reverse('product_object_detail', kwargs = {'object_id':self.pk})

#Location related models

class GeneLocation(LocationMixin):
    Gene = models.ForeignKey('Gene')
    Genome = models.ForeignKey(Genome)

class ProductLocation(models.Model):
    Product = models.ForeignKey('Product')
    Gene = models.ForeignKey('Gene')






    
    






