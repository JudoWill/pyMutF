# Create your views here.
import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import date_based, list_detail
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.utils import simplejson

from models import *

#Abstract views!
class BaseViews(object):

    model = Genome
    template_root_path = None
    required_ids = ()
    pageinate_by = None
    default_slug = 'gene-id'

    def object_list(self, request):

        queryset = self.model.objects.all()

        info_dict = {
            'queryset':queryset,
            'template_name':'%s/object_list.html' % self.template_root_path,
        }

        return list_detail.object_list(request, **info_dict)

    def object_detail(self, request, object_id = None):


        queryset = self.model.objects.all()

        info_dict = {
            'queryset':queryset,
            'object_id':object_id,
            'template_name':'%s/detail.html' % self.template_root_path,
        }

        return list_detail.object_detail(request, **info_dict)

    def add_from_ncbi(self, request, *args, **kwargs):
        pass



#Real views!!!
class OrganismViews(BaseViews):
    template_root_path = 'organism'
    model = Organism
    required_ids = ('tax-id',)

class GenomeViews(BaseViews):
    template_root_path = 'genome'
    model = Genome
    required_ids = ('tax-id',)

class GeneViews(BaseViews):
    template_root_path = 'gene'
    model = Gene
    required_ids = ('tax-id','gene-id')

class ProductViews(BaseViews):
    template_root_path = 'product'
    model = Product
    required_ids = ('tax-id','gene-id')