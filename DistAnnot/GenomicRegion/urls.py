from django.conf.urls.defaults import *
from django.views.generic import list_detail
from views import *

#Abstract patterns
class UrlPatternsBase(object):
    url_name_root = None
    admin_prefix = 'admin' #TODO: This is probably not right to use something like that to figure out the admin url path. Maybe use the reverse function?
    views = None

class NCBIPatterns(UrlPatternsBase):

    def get_url_patterns(self):
        return self.get_add_from_ncbi() + self.get_list_patterns() + self.get_detail_patterns()

    def get_add_from_ncbi(self):
        return patterns('',
                        url('%s/add_from_pubmed.html' % self.url_name_root,
                            self.views.add_from_ncbi,
                            name = '%s_add_from_pubmed' % self.url_name_root))

    def get_list_patterns(self):
        return patterns('',
                        url('%s/object_list/' % self.url_name_root,
                            self.views.object_list,
                            name = '%s_object_list' % self.url_name_root))

    def get_detail_patterns(self):
        return patterns('',
                        url('%s/detail-(?P<object_id>\d+).html' % self.url_name_root,
                            self.views.object_detail,
                            name = '%s_object_detail' % self.url_name_root))




#REAL PATTERNS!!!
class OrganismPatterns(NCBIPatterns):
    url_name_root = 'organism'
    views = OrganismViews()

class GenomePatterns(NCBIPatterns):
    url_name_root = 'genome'
    views = GenomeViews()

class GenePatterns(NCBIPatterns):
    url_name_root = 'gene'
    views = GeneViews()

class ProductPatterns(NCBIPatterns):
    url_name_root = 'product'
    views = ProductViews()


urlpatterns = OrganismPatterns().get_url_patterns()
urlpatterns += GenomePatterns().get_url_patterns()
urlpatterns += GenePatterns().get_url_patterns()
urlpatterns += ProductPatterns().get_url_patterns()
