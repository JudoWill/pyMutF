from django.db import models

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
    is_required = models.BooleanField(default = False)

    def __unicode__(self):
        return self.Type

#Organism Related models

class Organism(NameMixin):
    pass

class Genome(NameMixin):
    Organism = models.ForeignKey(Organism)

#Gene/Product related Models

class Gene(NameMixin, ProductMixin):
    Genome = models.ManyToManyField(Genome, through = 'GeneLocation')

class Product(NameMixin):
    Gene = models.ManyToManyField(Gene, through = 'ProductLocation')

#Location related models

class GeneLocation(LocationMixin):
    Gene = models.ForeignKey('Gene')
    Genome = models.ForeignKey(Genome)

class ProductLocation(models.Model):
    Product = models.ForeignKey('Product')
    Gene = models.ForeignKey('Gene')






    
    






