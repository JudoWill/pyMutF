from django.forms import ModelForm
from django import forms
from DistAnnot.Annot.models import MutationAnnot
from DistAnnot.Interaction.models import Gene, InteractionType, EffectType
from DistAnnot.Interaction.widgets import *
from DistAnnot.Annot.widgets import *

from autocomplete.fields import ModelChoiceField

class AnnotForm(forms.Form):

    Bad_extraction = forms.BooleanField(required = False, label = 'Bad Extraction?',
                                        help_text = 'Check this box if the text displayed is just jibberish')
    No_mutation = forms.BooleanField(required = False, label = 'No Mutation mentioned?',
                                     help_text = 'Check this box if there are no mentions of a mutation in this text')
    MentionedGenes = MultiChoiceGeneField(Gene.objects.all(), required = False, label = 'Genes Mentioned')
    MutatedGene = ChoiceGeneField(Gene.objects.all(), required = False, label = 'Mutated Gene')
    SentenceID = forms.IntegerField(widget = forms.HiddenInput)
    MutID = forms.IntegerField(widget = forms.HiddenInput)
    

class InteractionEffectForm(forms.Form):
    
    id = forms.IntegerField(widget = forms.HiddenInput)
    EffectChoice = forms.ModelChoiceField(queryset = EffectType.objects.all(), required = False,
                                            empty_label="No Effect", label = 'Effect on the Interaction')
    EffectFreeText = forms.CharField(widget = forms.Textarea, max_length = 256, required = False,
                                     label = 'Free Text of effect on the Interaction')


class GeneAnnotForm(forms.Form):

    Gene = ModelChoiceField('gene', required = False)
    is_mutated = forms.BooleanField(required = False)

