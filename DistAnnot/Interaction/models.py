from django.db import models
from DistAnnot.PubmedUtils import GetXML
from BeautifulSoup import BeautifulStoneSoup 

# Create your models here.
class Sentence(models.Model):

    Text = models.TextField()
    PMID = models.IntegerField()
    ParNum = models.IntegerField(blank = True, default = None, null = True)
    SentNum = models.IntegerField(blank = True, default = None, null = True)
    Interactions = models.ManyToManyField('Interaction')
    Genes = models.ManyToManyField('Gene', through = 'GeneAnnotation')
    Mutation = models.ManyToManyField('Mutation')
    Article = models.ForeignKey('Article', null = True, default = None)

    def __unicode__(self):
        
        return '<Sentence:%d:%d:%d>' % (self.Article.PMID, self.ParNum, 
                                        self.SentNum)

class Interaction(models.Model):

    HIVGene = models.ForeignKey('Gene', related_name = 'HIVPartner',
                                limit_choices_to = {'Organism__eq':'HIV'})
    HumanGene = models.ForeignKey('Gene', related_name = 'HumanPartner',
                                limit_choices_to = {'Organism__eq':'Human'})
    InteractionType = models.ForeignKey('InteractionType')

    def __unicode__(self):
        
        return '<Interaction:%s:%s:%s>' % (str(self.HIVGene),
                                            str(self.HumanGene),
                                            str(self.InteractionType))

class Mutation(models.Model):

    Mut = models.CharField(max_length = 20)
    Gene = models.ForeignKey('Gene', blank = True, null = True)
    Interaction = models.ManyToManyField(Interaction, through = 'InteractionEffect')

    def __unicode__(self):
        
        return '<Mutation:%s:%s>' % (self.Mut, str(self.Gene))

class InteractionEffect(models.Model):

    Interaction = models.ForeignKey('Interaction')
    Mutation = models.ForeignKey('Mutation')
    EffectType = models.ForeignKey('EffectType', null = True)

class Gene(models.Model):

    Organism = models.CharField(max_length = 256)
    Name = models.CharField(max_length = 256)
    Entrez = models.IntegerField()
    ExtraNames = models.ManyToManyField('ExtraGeneName')

class ExtraGeneName(models.Model):
    
    Name = models.CharField(max_length = 256)

class GeneAnnotation(models.Model):
    
    Sentence = models.ForeignKey('Sentence')
    Gene = models.ForeignKey('Gene')

class InteractionType(models.Model):

    Type = models.CharField(max_length = 256)

class EffectType(models.Model):
    Slug = models.SlugField(max_length = 256)
    Description = models.CharField(max_length = 256)

class Article(models.Model):

    PMID = models.IntegerField()
    PMCID = models.CharField(max_length = 20, blank=True, null = True,
                             default = None)
    PubMedXML = models.XMLField(null = True, default = None)
    PMCXML = models.XMLField(null = True, default = None)
    HasMut = models.NullBooleanField(default = None)

    def GetPubMedXML(self, cache_only = False):
        if self.PubMedXML is None and not cache_only:
            try:
                temp = GetXML([str(self.PMID)])
                soup = BeautifulStoneSoup(temp)
                self.PubMedXML = soup.prettyify()
            except:
                pass
            
        return self.PubMedXML

    def GetPMCXML(self, cache_only = False):
        if self.PMCXML is None and not cache_only:
            try:
                temp = GetXML([str(self.PMCID)], db = 'pmc')
                soup = BeautifulStoneSoup(temp)
                self.PMCXML = soup.prettyify()
            except:
                pass
        return self.PMCXML




    