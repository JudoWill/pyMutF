from django.forms import ModelForm
from django import forms
from DistAnnot.Annot.models import MutationAnnot
from DistAnnot.Interaction.models import Gene, InteractionType, EffectType
from DistAnnot.Interaction.widgets import *




class MutationSearch(forms.Form):
    lines = forms.CharField(widget = forms.Textarea, label = 'Query')
    allow = forms.BooleanField(required = False, label = 'Allow Unlabeled?')
    csv_format = forms.BooleanField(required = False, label = 'Return as CSV format')


class MutationTag(forms.Form):
    Slug = forms.SlugField()
