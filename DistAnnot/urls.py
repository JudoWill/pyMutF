from django.conf.urls.defaults import *
from django.conf import settings

from Interaction.models import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from autocomplete.views import autocomplete

autocomplete.register(
    id = 'gene',
    queryset = Gene.objects.all(),
    fields = ('Name', 'Entrez', 'ExtraNames__Name'),
    limit = 5
)
autocomplete.register(
    id = 'tag',
    queryset = MutationTags.objects.all(),
    fields = ('Slug',),
    limit = 5
)

urlpatterns = patterns('',
    # Example:
    # (r'^DistAnnot/', include('DistAnnot.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^pymutf/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^pymutf/admin/', include(admin.site.urls)),
	url(r'^pymutf/login.html', 'django.contrib.auth.views.login', name = 'login'),
	url(r'^pymutf/logout.html', 'django.contrib.auth.views.logout', name = 'logout'),
    url(r'^pymutf/index.html', 'Interaction.views.index', name = 'home'),
	(r'^pymutf/interactions/', include('Interaction.urls')),
    (r'^pymutf/annotations/', include('Annot.urls')),
    (r'^pymutf/Genomes/', include('GenomicRegion.urls')),
    url('^pymutf/autocomplete/(\w+)/$', autocomplete, name='autocomplete')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^pymutf/site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_FILE_ROOT}),
        (r'^pymutf/js/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_FILE_ROOT+'/js/'})
    )