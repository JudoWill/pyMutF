from django import forms
from DistAnnot.Interaction.models import Gene
from DistAnnot.Annot.widgets import AutoCompleteTagInput, AutoCompleteTagInputLarge

from operator import attrgetter
from django.db.models.query_utils import Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist



class ChoiceGeneField(forms.ModelChoiceField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        self.mapping = {    'GN':attrgetter('Name'),
                            'EN':attrgetter('Entrez'),
                            'ON':lambda x:list(x.ExtraNames.all())}
        
        self.qresolve = {   'GN': lambda x: Q(Name=x),
                            'EN': lambda x: Q(Entrez=int(x)),
                            'ON': lambda x: Q(ExtraNames__Name=x)}
        kwargs['widget'] = AutoCompleteTagInput(attrs = {'queryset':queryset,
                                                         'mapping':self.mapping})
        kwargs['queryset'] = queryset
        super(ChoiceGeneField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        if not value:
            return None
        print value
        vparts = value.split(':')
        try:
            typ = vparts[0]
            ref = vparts[1].split(',')[0]
        except IndexError:
            return None

        Qgen = self.qresolve[typ]
        Qobj = Qgen(ref)
        try:
            obj = Gene.objects.get(Qobj)
        except MultipleObjectsReturned:
            obj = Gene.objects.filter(Qobj)[0]
        except ObjectDoesNotExist:
            obj = None
        return obj
    def validate(self, value):
        pass


class MultiChoiceGeneField(ChoiceGeneField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        self.mapping = {    'GN':attrgetter('Name'),
                            'EN':attrgetter('Entrez'),
                            'ON':lambda x:list(x.ExtraNames.all())}

        self.qresolve = {   'GN': lambda x: Q(Name=x),
                            'EN': lambda x: Q(Entrez=int(x)),
                            'ON': lambda x: Q(ExtraNames__Name=x)}
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
            try:
                typ = vparts[0]
                ref = vparts[1]
            except IndexError:
                continue

            Qgen = self.qresolve[typ]
            Qobj = Qgen(ref)
            try:
                obj = Gene.objects.get(Qobj)
            except MultipleObjectsReturned:
                obj = Gene.objects.filter(Qobj)[0]
            except ObjectDoesNotExist:
                continue
            ids.append(obj.id)
        return Gene.objects.filter(id__in = ids).distinct()