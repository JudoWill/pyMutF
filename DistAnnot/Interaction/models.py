from django.db import models

# Create your models here.
class Sentence(models.Model):

    Text = models.TextField()
    PMID = models.IntegerField()
    ParNum = models.IntegerField(blank = True, default = None)
    Interactions = models.ForeignKey('Interaction')
    Genes = models.ManyToManyField('Gene')


class Interaction(models.Model):

    HIVGene = models.ForeignKey('Gene', related_name = 'HIVPartner',
                                limit_choices_to = {'Organism__eq':'HIV'})
    HumanGene = models.ForeignKey('Gene', related_name = 'HumanPartner',
                                limit_choices_to = {'Organism__eq':'Human'})
    InteractionType = models.ForeignKey('InteractionType')

class Mutation(models.Model):

    Mut = models.CharField(max_length = 20)
    Gene = models.ForeignKey('Gene')
    Interaction = models.ManyToManyField(Interaction, through = 'InteractionEffect')

class InteractionEffect(models.Model):

    Interaction = models.ForeignKey('Interaction')
    Mutation = models.ForeignKey('Mutation')
    Type = models.CharField(max_length = 256)

class Gene(models.Model):

    Organism = models.CharField(max_length = 256)
    Name = models.CharField(max_length = 256)
    Entrez = models.IntegerField()

class InteractionType(models.Model):

    Type = models.CharField(max_length = 256)