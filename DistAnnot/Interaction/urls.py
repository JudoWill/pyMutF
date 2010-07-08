from django.conf.urls.defaults import *
from django.views.generic import list_detail
from DistAnnot.Interaction.models import *


# Uncomment the next two lines to enable the admin:




urlpatterns = patterns('',
     url(r'^stats.html', 'Interaction.views.stats', name = 'stats'),
     url(r'^mutations/$', 'Interaction.views.mutation_list', name = 'mutation_list'),
     url(r'^gene_list.html', 'Annot.views.gene_list', name = 'gene_list'),
)
