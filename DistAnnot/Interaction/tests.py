"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from DistAnnot.Interaction.models import *



class SimpleTest(TestCase):
    def test_article_retrieval(self):

        test_articles = [ {'PMID':14694110, 'PMCID':'PMC368750', 'res':'K298A'},
                              {'PMID':10074138, 'PMCID':'PMC104048', 'res':'F16A'}]

        for art in test_articles:
            nart = Article(PMID = art['PMID'], PMCID = art['PMCID'])
            nart.ReadMuts()
            self.assertTrue(Mutation.objects.filter(Mut = art['res']).exists())