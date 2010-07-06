from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import list_detail
# Create your views here.

from DistAnnot.Interaction.models import *
from DistAnnot.Annot.models import *
from DistAnnot.Queries.models import *


def index(request):

    return render_to_response('index.html', 
			context_instance = RequestContext(request))

@login_required
def stats(request):

    data = []

    data.append({'Title':'Number of Articles',
                 'value':Article.objects.all().count()})
    data.append({'Title':'Number of Sentences',
                 'value':Sentence.objects.all().count()})
    data.append({'Title':'Number of Sentences with Mutations',
                 'value':Sentence.objects.annotate(num_mut = Count('Mutation')).filter(num_mut__gte = 1).count()})
    data.append({'Title':'Number of Annotated Mutations',
                 'value':Mutation.objects.filter(Gene__isnull = False).count()})

    cdict = {'data':data}

    return render_to_response('Interaction/stats.html', cdict,
                              context_instance = RequestContext(request))

def mutation_list(request):

    response = list_detail.object_list(
        request,
        queryset = Mutation.objects.all().order_by('Mut', '-Interaction'),
        template_name = 'Interaction/Mutation_list.html'
    )

    return response