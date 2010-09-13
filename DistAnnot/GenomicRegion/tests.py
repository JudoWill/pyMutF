"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from views import *

class GenomeViewsTest(TestCase):
    fixtures = ['smallhiv']
    view_class = GenomeViews()
    model = Genome
    base_id = 'refseq'
    msg_prefix = 'genome'

    def get_object_list_url(self):
        return '/Genomes/genome/object_list/'

    def test_list_by_slug(self):
        resp = self.client.get(self.get_object_list_url())
        #annoying hack of hard-coding, cant seem to get around it though!
        for object in self.model.objects.all():
            off_sym = object.get_official_symbol().Name
            off_name = object.get_official_name().Name
            self.assertContains(resp, off_sym,
                                msg_prefix = self.msg_prefix)
            self.assertContains(resp, off_name,
                                msg_prefix = self.msg_prefix)

    def test_detail(self):
        for object in self.model.objects.all():
            resp = self.client.get(object.get_absolute_url())
            for name in object.Names.all():
                self.assertContains(resp, name.Name,
                                    msg_prefix = self.msg_prefix)


class GeneViewsTest(GenomeViewsTest):

    view_class = GeneViews()
    model = Gene
    base_id = 'refseq'
    msg_prefix = 'gene'

    def get_object_list_url(self):
        return '/Genomes/gene/object_list/'