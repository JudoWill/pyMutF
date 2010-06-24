from django.forms import ModelForm
from django import forms
from DistAnnot.Annot.models import MutationAnnot
from DistAnnot.Interaction.models import Gene
from widgets import AutoCompleteTagInput


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
    SentenceID = forms.IntegerField(widget = forms.HiddenInput)
    
    def clean(self):

        cleaned_data = self.cleaned_data
        cleaned_data['Bad_extraction'] = cleaned_data['Bad_extraction'].strip()[:-1]
        cleaned_data['No_mutation'] = cleaned_data['No_mutation'].strip()[:-1]        

        if cleaned_data['Bad_extraction'] or cleaned_data['No_mutation']:
            return cleaned_data
        
        if len(cleaned_data['Human_gene']) == 0 and len(cleaned_data['HIV_gene']) == 0:
            raise forms.ValidationError('You must specify at least ONE protein')

        if cleaned_data['Human_gene'] and cleaned_data['HIV_gene']:
            raise forms.ValidationError('You can only specify ONE protein')

        return cleaned_data