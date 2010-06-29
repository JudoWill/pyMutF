from django.db import models
from DistAnnot.Interaction.models import Article
from PubmedUtils import SearchPUBMED
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from itertools import product

# Create your models here.
from DistAnnot.PubmedUtils import SearchPUBMED

class QueryRule(models.Model):

    Slug = models.SlugField(max_length = 256)
    QueryRule = models.CharField(max_length = 256)
    Queries = models.ManyToManyField('Query')
    Data = models.ManyToManyField('Data')

    def __unicode__(self):
        return '<QueryRule:%s>' % self.Slug

    def YieldQueries(self):
        """Yields rendered queries based on the data provided"""
        datatypes = self.Data.values_list('identifier', flat = True).distinct()

        if len(datatypes) == 1:
            for data in self.Data.all():
                yield self.render({datatypes[0]:data}), data

        qsets = []
        for dtype in datatypes:
            qsets.append(self.Data.filter(identifier = dtype))

        for data_group in product(*qsets):
            yield self.render(dict(zip(datatypes, data_group))), data_group

    def render(self, data_dict):
        """Renders a query based on the data passed"""

        render_dict = {}
        for key, item in data_dict.values():
            render_dict[key] = item.content_object.to_query()

        return self.QueryRule % render_dict


class Data(models.Model):

    identifier = models.CharField(max_length = 256)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    ShouldLink = models.BooleanField(default = False)

    def __unicode__(self):

        return '<Data:%s:%s>' % (self.identifier, self.content_object.to_query())




class Query(models.Model):

    QueryText = models.CharField(max_length = 256)
    DataObjects = models.ManyToManyField('Data')
    Articles = models.ManyToManyField(Article)
    DateAdded = models.DateField(auto_now_add = True)
    LastChecked = models.DateTimeField(auto_now = True)

    def __unicode__(self):

        return '<Query:%s>' % self.QueryText


    def DoQuery(self, USE_RECENT = True):
        """Searches the Pubmed interface and returns PMIDS for all of the retrieved article"""
        if USE_RECENT:
            return SearchPUBMED(self.QueryText, recent_date = self.LastChecked)
        else:
            return SearchPUBMED(self.QueryText, recent_date = None)
        


