from django import forms
from django.conf import settings
from django.utils import simplejson
from django.utils.safestring import mark_safe


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
        tag_items = []
        for item in qset:
            for key, fun in mapping.items():
                tag_items.append(key+':'+str(fun(item)))
        tag_list = simplejson.dumps(tag_items,
                                    ensure_ascii=False)
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
            </script>''' % (name, tag_list))