from django import forms
from django.utils import simplejson
from django.utils.safestring import mark_safe


class AutoCompleteTagInput(forms.TextInput):
    class Media:
        css = {
            'all': ('jquery.autocomplete.css',)
        }
        js = (
            'lib/jquery.js',
            'lib/jquery.bgiframe.min.js',
            'lib/jquery.ajaxQueue.js',
            'jquery.autocomplete.js'
        )

    def render(self, name, value, attrs=None):
        """Must be passed a ValueQuerySet!!!"""
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)

        qset = attrs['queryset']
        tag_items = []
        for item in qset:
            for val in item.values():
                tag_items.append(str(val))
        tag_list = simplejson.dumps(tag_items,
                                    ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 150,
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