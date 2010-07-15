from django import forms
from DistAnnot.Interaction.models import Gene, MutationTags
from DistAnnot.Annot.widgets import AutoCompleteTagInput, AutoCompleteTagInputLarge
from django.conf import settings
from django.utils import simplejson
from django.utils.safestring import mark_safe

from operator import attrgetter
from django.db.models.query_utils import Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist



def MakeString(name, json_obj):

    outstr = mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%(name)s").autocomplete(%(json)s, {
                width: 700,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % {'name':name, 'json':json_obj})

    return outstr

class AutoCompleteMutationTagInput(forms.TextInput):
    class Media:
        css = {
            'all': (settings.MEDIA_URL+'/'+'jquery.autocomplete.css',)
        }
        js = (
            settings.MEDIA_URL+'/'+'lib/jquery.js',
            settings.MEDIA_URL+'/'+'lib/jquery.bgiframe.min.js',
            settings.MEDIA_URL+'/'+'lib/jquery.ajaxQueue.js',
            settings.MEDIA_URL+'/'+'jquery.autocomplete.js'
        )

    def render(self, name, value, attrs=None):
        """Must be passed a QuerySet!!!"""
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)


        json_data = simplejson.dumps()
        return output +  MakeString(name, json_data)


class ChoiceTagField(forms.ModelChoiceField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        kwargs['widget'] = AutoCompleteMutationTagInput(attrs = {'queryset':queryset})
        kwargs['queryset'] = queryset
        super(ChoiceGeneField, self).__init__(*args, **kwargs)

    def to_python(self, value):
            if not value:
                return None

            id_list = []
            for slug in value.split(','):
                try:
                    tag, isnew = MutatationTags.objects.get_or_create(Slug__iexact = slug.strip())
                except MultipleObjectsReturned:
                    tag = MutatationTags.filter(Slug__iexact = slug.strip())[0]

                id_list.append(tad.id)


            return MutationTags.objects.filter(pk__in = id_list)
        def validate(self, value):
            pass





class ChoiceGeneField(forms.ModelChoiceField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset.select_related('ExtraNames')
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
        self.queryset = queryset.select_related('ExtraNames')
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