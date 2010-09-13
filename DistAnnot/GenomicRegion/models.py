from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


#Abstract Models

class NameMixin(models.Model):
    Names = models.ManyToManyField('Name')

    class Meta:
        abstract = True

    def get_offical_symbol(self):
        return self.Names.objects.get(NameType = 'Official Symbol')

    def __unicode__(self):
        return self.get_offical_symbol().Name
        
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
    pass

    def get_absolute_url(self):
        return reverse('organism_object_detail', kwargs = {'object_id':self.pk})

class Genome(NameMixin):
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






    
    






