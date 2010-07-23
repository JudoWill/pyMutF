"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from DistAnnot.Interaction.models import *
from DistAnnot.PubmedUtils import *



class TestRetrieval(TestCase):

    def test_article_retrieval(self):

        test_articles = [ {'PMID':14694110, 'PMCID':'PMC368750', 'res':'K298A'},
                              {'PMID':10074138, 'PMCID':'PMC104048', 'res':'F16A'}]

        for art in test_articles:
            nart = Article(PMID = art['PMID'], PMCID = art['PMCID'])
            nart.ReadMuts()
            self.assertTrue(Mutation.objects.filter(Mut = art['res']).exists())

    def test_list_retrieval_PMID(self):

        test_articles = [14694110, 10074138]
        for art, id in GetXMLfromList(test_articles):
            print id
            self.assertTrue(int(id) in test_articles)
        
    def test_list_retrieval_PMCID(self):

        test_articles = ['PMC368750', 'PMC104048']
        for art, id in GetXMLfromList(test_articles, db = 'pmc'):
            print id
            self.assertTrue(id in test_articles)


class GenericViews(TestCase):

    fixtures = ['test_Article', 'test_Interaction', 'test_Mutation',
                'test_Reference', 'test_MutationTags', 'test_Sentence']

    def test_article_detail(self):

        for art in Article.objects.all():
            resp = self.client.get(art.get_absolute_url())
            self.failUnlessEqual(resp.status_code, 200)
            for sent in art.sentence_set.all():
                self.assertContains(resp, sent.Text)

    def test_tag_detail(self):

        for tag in MutationTags.objects.all():
            resp = self.client.get(tag.get_absolute_url())
            for mut in tag.mutation_set.all():
                self.assertContains(resp, mut.Mut)

    def test_tag_list(self):

        resp = self.client.get(reverse('tag_list'))
        for mut in MutationTags.objects.all():
            self.assertContains(resp, mut.Slug)

