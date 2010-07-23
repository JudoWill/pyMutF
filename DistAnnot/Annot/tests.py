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

    


        



