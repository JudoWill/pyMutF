"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from DistAnnot.Interaction.models import *
from forms import AnnotForm, InteractionEffectForm
from django.forms.formsets import formset_factory

class SimpleTest(TestCase):
    
    fixtures = ['Interaction.simple_data.yaml']

    def test_jibberish(self):
        print Article.objects.all().count()
        sent = Sentence.objects.all()[0]
        mut = sent.Mutation.all()[0]

        data = {'effect-SentenceID': sent.id,
                'effect-MutID': mut.id,
                'effect-BadExtraction':True}


        resp = self.client.post(reverse('LabelMutation'), data)

        self.assertFalse(Sentence.objects.filter(id = sent.id).exists())


        



