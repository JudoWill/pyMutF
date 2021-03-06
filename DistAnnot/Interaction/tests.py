"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from DistAnnot.Interaction.models import *
from DistAnnot.PubmedUtils import *
from django.contrib.auth.models import User, UserManager



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

    def test_mutation_detail(self):

        for mut in Mutation.objects.all():
            resp = self.client.get(mut.get_absolute_url())
            self.assertContains(resp, mut.Gene.Name)
            for art in mut.GetArticles():
                self.assertContains(resp, str(art.PMID))

    def test_gene_detail(self):

        for gene in Gene.objects.all():
            resp = self.client.get(gene.get_absolute_url())
            self.assertContains(resp, gene.Name)
            for mut in gene.mutation_set.all():
                self.assertContains(resp, mut.Mut)

            tstr = 'Mentioned in %i articles.' % gene.GetArticle().count()
            self.assertContains(resp, tstr)

    def test_mutation_list(self):

        resp = self.client.get(reverse('mutation_list'))
        for mut in Mutation.objects.all():
            self.assertContains(resp, mut.Mut)
            self.assertContains(resp, mut.Gene.Name)
            for desc in mut.Descriptions.all():
                self.assertContains(resp, desc.Slug)


    def test_tag_mutation(self):

        for mut in Mutation.objects.all():
            resp = self.client.get(reverse('mutation_tag',
                                           kwargs={'object_id':mut.pk}))
            for sent in mut.sentence_set.all():
                self.assertContains(resp, sent.Text)
            for art in mut.GetArticles():
                self.assertContains(resp, str(art.PMID))

    def test_stats(self):

        check_sents = ('Number of Articles', 'Number of Sentences',
                       'Number of Sentences with Mutations',
                       'Number of Annotated Mutations',)
        user = User.objects.create_user('tuser', 'test@test.com', 'test')
        user.save()
        self.client.login(username = 'tuser', password = 'test')
        resp = self.client.get(reverse('stats'))
        for sent in check_sents:
            self.assertContains(resp, sent)
