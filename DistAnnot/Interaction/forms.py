from django.forms import ModelForm
from django import forms
from DistAnnot.Annot.models import MutationAnnot
from DistAnnot.Interaction.models import *
from DistAnnot.Interaction.widgets import *

from autocomplete.fields import ModelChoiceField



class MutationSearch(forms.Form):
    lines = forms.CharField(widget = forms.Textarea, label = 'Query')
    allow = forms.BooleanField(required = False, label = 'Allow Unlabeled?')
    csv_format = forms.BooleanField(required = False, label = 'Return as CSV format')
    order = forms.CharField(label = 'Field Order')


class MutationTagForm(forms.Form):

    Tags = ChoiceTagField(queryset = MutationTags.objects.all())
    Article = forms.IntegerField(widget = forms.HiddenInput)

class GeneAnnotForm(forms.Form):

    Gene = ModelChoiceField('gene', required = False)
    is_mutated = forms.BooleanField(required = False)


class RefForm(forms.Form):
    NewTag = models.CharField(required = False)
    Tag = ModelChoiceField('tag', required = False)
    
