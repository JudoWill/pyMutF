from django.db import models
from django.core.urlresolvers import reverse
from django.core.cache import cache
import django.db.transaction

from DistAnnot.PubmedUtils import *
from BeautifulSoup import BeautifulStoneSoup
from nltk.tokenize import sent_tokenize
from itertools import count, izip
import DistAnnot.settings as settings
import os

# Create your models here.
from DistAnnot.mutation_finder import mutation_finder_from_regex_filepath as mutfinder_gen

class Sentence(models.Model):

    Text = models.TextField()
    PMID = models.IntegerField(null = True)
    ParNum = models.IntegerField(blank = True, default = None, null = True)
    SentNum = models.IntegerField(blank = True, default = None, null = True)
    Genes = models.ManyToManyField('Gene', through = 'GeneAnnotation')
    Mutation = models.ManyToManyField('Mutation')
    Article = models.ForeignKey('Article', null = True, default = None)
    Priority = models.IntegerField(null = True, default = None)
    RandOrder = models.FloatField(null = True, default = None)

    def __unicode__(self):

        return '%s:%s:%s' % (str(self.Article.PMID), str(self.ParNum),
                                        str(self.SentNum))

class Interaction(models.Model):

    HIVGene = models.ForeignKey('Gene', related_name = 'HIVPartner',
                                limit_choices_to = {'Organism__eq':'HIV'})
    HumanGene = models.ForeignKey('Gene', related_name = 'HumanPartner',
                                limit_choices_to = {'Organism__eq':'Human'})
    InteractionType = models.ForeignKey('InteractionType')

    class Meta:
        get_latest_by = 'HIVGene'

    def __unicode__(self):
        
        return '%s:%s:%s' % (str(self.HIVGene),
                            str(self.HumanGene),
                            str(self.InteractionType))

    def to_query(self):
        temp = '%s interacts %s' % (self.HIVGene.Name,
                                                self.HumanGene.Name)
        return temp.replace(' ', '+')


class Mutation(models.Model):

    Mut = models.CharField(max_length = 20)
    Gene = models.ForeignKey('Gene', blank = True, null = True)
    Interaction = models.ManyToManyField(Interaction, through = 'InteractionEffect')
    Position = models.IntegerField(default = None, null = True)
    Descriptions = models.ManyToManyField('MutationTags', through = 'Reference')

    def __unicode__(self):
        
        return '%s:%s' % (self.Mut, str(self.Gene))

    def get_absolute_url(self):

        return reverse('mutation_detail', kwargs = {'object_id':self.pk})


    @django.db.transaction.commit_on_success
    def JoinMuts(self, *args):

        for mut in args:
            assert self.Mut == mut.Mut, 'Mutations do not match!!'
            assert self.Gene == mut.Gene, 'Genes do mot match!!'

            effects = InteractionEffect.objects.filter(Mutation = mut)
            for effect in effects:
                effect.Mutation = self
                effect.save()

            for sent in mut.sentence_set.all():
                self.sentence_set.add(sent)
            mut.delete()
            

    def GetEffect(self):

        id = cache.get('mutval-%i' % self.pk)
        if id is None:
            if InteractionEffect.objects.filter(Mutation = self).exists():
                id = InteractionEffect.objects.filter(Mutation = self)[0].id
            else:
                id = 0
            cache.set('mutval-%i' % self.pk, id, 30 * 60)

        if id != 0:
            return InteractionEffect.objects.get(id = id)
        else:
            return None

    def GetLabelUrl(self):
        url = cache.get('muturl-%i' % self.pk)
        if url is None:
            if self.sentence_set.exists():
                url = reverse('LabelNewMutation',
                               kwargs = {'SentID': self.sentence_set.all()[0].id,
                                         'MutID': self.id})
            else:
                url = ''
            cache.set('muturl-%i' % self.pk, url, 30 * 60)
        return url

    def GetArticles(self):

        arts = []
        for sent in self.sentence_set.all():
            arts += [sent.Article.id]

        return Article.objects.filter(id__in = arts)

class Reference(models.Model):
    Article = models.ForeignKey('Article')
    Mutation = models.ForeignKey('Mutation')
    Tag = models.ForeignKey('MutationTags')

    def __unicode__(self):

        return ':'.join([str(self.Article), str(self.Mutation), str(self.Tag)])
        



class MutationTags(models.Model):
    Slug = models.SlugField()
    Description = models.TextField()

    def __unicode__(self):
        return self.Slug

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs = {'object_id':self.pk})


class InteractionEffect(models.Model):

    Interaction = models.ForeignKey('Interaction')
    Mutation = models.ForeignKey('Mutation')
    EffectType = models.ForeignKey('EffectType', null = True)

    def __unicode__(self):
        
        return '%s:%s:%s' % (str(self.Interaction), str(self.Mutation),
                            str(self.EffectType))

class Gene(models.Model):

    Organism = models.CharField(max_length = 256)
    Name = models.CharField(max_length = 256)
    Entrez = models.IntegerField()
    ExtraNames = models.ManyToManyField('ExtraGeneName')

    def __unicode__(self):

        return '%s:%s' % (str(self.Entrez), self.Name)

    def get_absolute_url(self):

        return reverse('gene_detail', kwargs = {'object_id':self.pk})

    def to_query(self):

        return self.Name

    def GetArticle(self):

        return self.sentence_set.values('Article').distinct()

class ExtraGeneName(models.Model):
    
    Name = models.CharField(max_length = 256)

    def __unicode__(self):
        return self.Name

    def to_query(self):

        return self.Name

class GeneAnnotation(models.Model):
    
    Sentence = models.ForeignKey('Sentence')
    Gene = models.ForeignKey('Gene')

    def __unicode__(self):

        return '%s:%s' % (str(self.Sentence), str(self.Gene))

class InteractionType(models.Model):

    Type = models.CharField(max_length = 256)

    def __unicode__(self):

        return '%s' % self.Type

class EffectType(models.Model):
    Slug = models.SlugField(max_length = 256)
    Description = models.CharField(max_length = 256)

    def __unicode__(self):
        
        return self.Slug

class Article(models.Model):

    PMID = models.IntegerField(null = True)
    PMCID = models.CharField(max_length = 20, blank=True, null = True,
                             default = None)
    PubMedXML = models.XMLField(null = True, default = None)
    PMCXML = models.XMLField(null = True, default = None)
    HasMut = models.NullBooleanField(default = None)
    Interactions = models.ManyToManyField(Interaction)
    Title = models.TextField(null = True, default = None)

    def __unicode__(self):
        
        return 'PMID:%d' % self.PMID
    def get_absolute_url(self):
    	return reverse('article_detail', kwargs = {'object_id':self.pk})
    

    def GetPubMedXML(self, cache_only = False):
        if self.PubMedXML is None and not cache_only:

            temp = GetXML([str(self.PMID)])
           
            soup = BeautifulStoneSoup(temp)
            self.PubMedXML = soup.prettify()

            
        return self.PubMedXML

    def GetPMCXML(self, cache_only = False):
        if self.PMCXML is None and not cache_only:

            temp = GetXML([str(self.PMCID)], db = 'pmc')
            soup = BeautifulStoneSoup(temp)
            self.PMCXML = soup.prettify()
            

        return self.PMCXML

    def GetTitle(self):

        if self.Title is None:
            xml = self.PubMedXML or self.PMCXML or None
            if xml is None:
                return None

            soup = BeautifulStoneSoup(xml)
            title = soup.find('articletitle')
            if title:
                self.Title = title.string.strip()
        return self.Title




    def ReadMuts(self, MutFinder = None):

        if MutFinder is None:
            MutFinder = mutfinder_gen(settings.HOME_DIR + os.sep + 'regex.txt')


        if self.HasMut == False:
            return

        pargen = None
        if self.PMCID is not None:
            xml = self.GetPMCXML()
            if xml:
                pargen = ExtractPMCPar(xml)

        elif self.PMID is not None:
            xml = self.GetPubMedXML()
            if xml:
                pargen = ExtractPubPar(xml)


        self.HasMut = False
        

        for par, parnum in izip(pargen, count(0)):
            sent_list = ['']+list(sent_tokenize(par))+['']
            for sentnum, sent in enumerate(sent_list):
                for mut, loc in MutFinder(sent).items():
                    self.HasMut = True
                    text = ' '.join(sent_list[sentnum-1:sentnum+1])
                    obj, isnew = Sentence.objects.get_or_create(Article = self,
                                                    ParNum = parnum,
                                                    SentNum = sentnum,
                                                    defaults = {'Text':text})


                    qset = obj.Mutation.filter(Mut = mut)
                    if not qset.exists() and mut is not None and isnew:
                        mut_obj = Mutation.objects.create(Mut = mut)
                        obj.Mutation.add(mut_obj)

    