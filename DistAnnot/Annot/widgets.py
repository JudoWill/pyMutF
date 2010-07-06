from django import forms
from django.conf import settings
from django.utils import simplejson
from django.utils.safestring import mark_safe
from types import ListType
import os.path


def MakeList(mapping, qset, location):

    if not os.path.exists(location):
        tlist = []
        for item in qset:
            for key, fun in mapping.items():
                val = fun(item)
                if type(val) is ListType:
                    for v in val:
                        tlist.append(key+':'+v.Name)
                else:
                    tlist.append(key+':'+str(val))
        with open(location, 'w') as handle:
            handle.write(simplejson.dumps(tlist, ensure_ascii = False))
    with open(location) as handle:
        return handle.read()



class AutoCompleteTagInput(forms.TextInput):
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

        qset = self.attrs['queryset']
        mapping = self.attrs['mapping']
        json_data = MakeList(mapping, qset, os.path.join(settings.STATIC_FILE_ROOT,
                                             'data', 'gene_names.json'))
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
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
            </script>''' % (name, json_data))

class AutoCompleteTagInputLarge(forms.Textarea):
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
        output = super(AutoCompleteTagInputLarge, self).render(name, value, attrs)

        qset = self.attrs['queryset']
        mapping = self.attrs['mapping']
        json_data = MakeList(mapping, qset, os.path.join(settings.STATIC_FILE_ROOT,
                                             'data', 'gene_names.json'))
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
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
            </script>''' % (name, json_data))