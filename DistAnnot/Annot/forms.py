from django.forms import ModelForm
from django import forms
from DistAnnot.Annot.models import MutationAnnot
from DistAnnot.Interaction.models import Gene
from widgets import AutoCompleteTagInput

from operator import attrgetter
from django.db.models.query_utils import Q


class ChoiceGeneField(forms.ModelChoiceField):

    def __init__(self, queryset, *args, **kwargs):

        self.queryset = queryset
        self.mapping = {'GN':attrgetter('Name'),
                        'EN':attrgetter('Entrez')}
        self.qresolve = {'GN': lambda x: Q(Name=x),
                         'EN': lambda x: Q(Entrez=int(x))}
        kwargs['widget'] = AutoCompleteTagInput(attrs = {'queryset':queryset,
                                                         'mapping':self.mapping})
        kwargs['queryset'] = queryset
        super(ChoiceGeneField, self).__init__(*args, **kwargs)


    def to_python(self, value):

        if not value:
            return None

        vparts = value.split(':')
        typ = vparts[0]
        ref = vparts[1].split(',')[0]
        
        Qgen = self.qresolve[typ]
        Qobj = Qgen(ref)
        return Gene.objects.get(Qobj)

    def validate(self, value):
        pass


class MutationAnnotForm(ModelForm):
    class Meta:
        model =  MutationAnnot
        exclude = ['User']

class AnnotForm(forms.Form):

    Bad_extraction = forms.BooleanField(required = False,
                                        help_text = 'Check this box if the text displayed is just jibberish')
    No_mutation = forms.BooleanField(required = False,
                                     help_text = 'Check this box if there are no mentions of a mutation in this text')
    Human_gene = ChoiceGeneField(Gene.objects.filter(Organism = 'Human'), required = False)
    HIV_gene = ChoiceGeneField(Gene.objects.filter(Organism = 'HIV'), required = False)
    SentenceID = forms.IntegerField(widget = forms.HiddenInput)
    MutID = forms.IntegerField(widget = forms.HiddenInput)
    
    def clean(self):

        cleaned_data = self.cleaned_data

        if cleaned_data['Bad_extraction'] or cleaned_data['No_mutation']:
            return cleaned_data
        
        if cleaned_data['Human_gene'] is None and cleaned_data['HIV_gene'] is None:
            raise forms.ValidationError('You must specify at least ONE protein')

        if cleaned_data['Human_gene'] and cleaned_data['HIV_gene']:
            raise forms.ValidationError('You can only specify ONE protein')

        return cleaned_data



