from django.forms import ModelForm
from django import forms
from DistAnnot.Annot.models import MutationAnnot
from DistAnnot.Interaction.models import Gene
from widgets import AutoCompleteTagInput,CustomJQueryACWidget
from autocomplete import ModelChoiceField

class MutationAnnotForm(ModelForm):
    class Meta:
        model =  MutationAnnot
        exclude = ['User']

class AnnotForm(forms.Form):

    Bad_extraction = forms.BooleanField(required = False,
                                        help_text = 'Check this box if the text displayed is just jibberish')
    No_mutation = forms.BooleanField(required = False,
                                     help_text = 'Check this box if there are no mentions of a mutation in this text')
    Human_gene = forms.CharField(required = False, max_length = 256,
                                 widget = AutoCompleteTagInput(attrs = {'queryset':Gene.objects.filter(Organism = 'Human').values('Name', 'Entrez')}))
    HIV_gene = forms.CharField(required = False, max_length = 256,
                                 widget = AutoCompleteTagInput(attrs = {'queryset':Gene.objects.filter(Organism = 'HIV').values('Name', 'Entrez')}))
    
