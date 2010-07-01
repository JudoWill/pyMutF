from django.contrib import admin
from DistAnnot.Queries.models import *

class QueryRuleAdmin(admin.ModelAdmin):
    pass


class QueryAdmin(admin.ModelAdmin):
    pass


admin.site.register(QueryRule, QueryRuleAdmin)
admin.site.register(Query, QueryAdmin)