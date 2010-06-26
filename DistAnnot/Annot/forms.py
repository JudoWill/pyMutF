from django.forms import ModelForm
from django import forms
from DistAnnot.Annot.models import MutationAnnot
from DistAnnot.Interaction.models import Gene, InteractionType, EffectType
from DistAnnot.Interaction.widgets import *
from DistAnnot.Annot.widgets import *

class AnnotForm(forms.Form):

    Bad_extraction = forms.BooleanField(required = False,
                                        help_text = 'Check this box if the text displayed is just jibberish')
    No_mutation = forms.BooleanField(required = False,
                                     help_text = 'Check this box if there are no mentions of a mutation in this text')
    MentionedGenes = MultiChoiceGeneField(Gene.objects.all(), required = False)
    MutatedGene = ChoiceGeneField(Gene.objects.all(), required = False)
    SentenceID = forms.IntegerField(widget = forms.HiddenInput)
    MutID = forms.IntegerField(widget = forms.HiddenInput)
    

class InteractionEffectForm(forms.Form):
    
    id = forms.IntegerField(widget = forms.HiddenInput)
    HIVGene = ChoiceGeneField(Gene.objects.all())
    InteractionType = forms.ModelChoiceField(queryset = InteractionType.objects.all())
    HumanGene = ChoiceGeneField(Gene.objects.all())
    EffectChoide = forms.ModelChoiceField(queryset = EffectType.objects.all(), 
                                            empty_label="No Effect")
    EffectFreeText = forms.CharField(max_length = 256)
