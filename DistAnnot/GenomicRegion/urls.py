from django.conf.urls.defaults import *
from django.views.generic import list_detail

class UrlPatternsBase(object):
    url_name_root = None
    admin_prefix = 'admin' #TODO: This is probably not right to use something like that to figure out the admin url path. Maybe use the reverse function?
    views = None
    feeds = None

class GenePatterns(UrlPatternsBase):

    def get_url_patterns(self):
        return self.get_add_from_ncbi() + self.get_list_patterns()

    def get_add_from_ncbi(self):
        return patterns('',
                        url('^add_from_pubmed.html',
                            self.views.add_from_ncbi,
                            name = '%s_add_from_pubmed' % self.url_name_root))

    def get_list_patterns(self):
        return patterns('',
                        url('list_by_(?P<slug>[-\w]+)',
                            self.views.list_by_slug,
                            name = '%s_list_by_slug' % self.url_name_root))        
    