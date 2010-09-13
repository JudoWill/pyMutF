"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from views import *

class GenomeViewsTest(TestCase):
    fixtures = ['smallhiv']
    view_class = GenomeViews
    model = Genome
    base_id = 'refseq'
    msg_prefix = 'genome'

    def test_list_by_slug(self):
        resp = self.client.get(reverse(self.view_class.list_by_slug,
                                       kwargs = {'slug':'refseq'}))
        for object in self.model.objects.all():
            for name in object.Names.all():
                self.assertContains(resp, name.Name,
                                    msg_prefix = self.msg_prefix)

    def test_detail(self):

        for object in self.model.objects.all():
            resp = self.client.get(object.get_absolute_url())
            for name in object.Names.all():
                self.assertContains(resp, name.Name,
                                    msg_prefix = self.msg_prefix)


