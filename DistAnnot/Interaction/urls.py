from django.conf.urls.defaults import *
from django.views.generic import list_detail, object_detail
from DistAnnot.Interaction.models import *


# Uncomment the next two lines to enable the admin:

article_info = {
	template_name = '/Interaction/article_detail.html',
	queryset = Article.objects.all(),
}


urlpatterns = patterns('',
     url(r'^stats.html', 'Interaction.views.stats', name = 'stats'),
     url(r'^mutations/$', 'Interaction.views.mutation_list', name = 'mutation_list'),
     url(r'^gene_list.html', 'Annot.views.gene_list', name = 'gene_list'),
     url(r'^mutation_search.html', 'Interaction.views.mutation_search', name = 'mutation_search'),
     url(r'^article/(?P<object_id>\d*)/detail.html', object_detail, article_info, name = 'article_detail')
)
