from django import forms
from DistAnnot.Interaction.models import Gene
from DistAnnot.Annot.widgets import AutoCompleteTagInput, AutoCompleteTagInputLarge

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
        print value
        vparts = value.split(':')
        typ = vparts[0]
        ref = vparts[1].split(',')[0]        
        Qgen = self.qresolve[typ]
        Qobj = Qgen(ref)
        return Gene.objects.get(Qobj)
    def validate(self, value):
        pass


class MultiChoiceGeneField(ChoiceGeneField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        self.mapping = {'GN':attrgetter('Name'),
                        'EN':attrgetter('Entrez')}
        self.qresolve = {'GN': lambda x: Q(Name=x),
                         'EN': lambda x: Q(Entrez=int(x))}
        kwargs['widget'] = AutoCompleteTagInputLarge(attrs = {'queryset':queryset,
                                                         'mapping':self.mapping})
        kwargs['queryset'] = queryset
        super(ChoiceGeneField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        if not value:
            return None

        labels = map(lambda x: x.lstrip().rstrip(), value.split(','))[:-1]
        ids = []
        print labels
        for label in labels:
            vparts = label.split(':')
            print label
            typ = vparts[0]
            ref = vparts[1]
            Qgen = self.qresolve[typ]
            Qobj = Qgen(ref)
            ids.append(Gene.objects.get(Qobj).id)
        return Gene.objects.filter(id__in = ids).distinct()