from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db.models import Q
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import list_detail
from django.views.decorators.cache import cache_page, never_cache
from csv import DictReader
from StringIO import StringIO
# Create your views here.

from DistAnnot.Interaction.models import *
from DistAnnot.Annot.models import *
from DistAnnot.Queries.models import *
from DistAnnot.Interaction.forms import *


def index(request):

    return render_to_response('index.html', 
			context_instance = RequestContext(request))

@cache_page(10)
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
@never_cache
def mutation_list(request):

    response = list_detail.object_list(
        request,
        queryset = Mutation.objects.all().order_by('Gene', 'Position', 'Mut', '-Interaction'),
        template_name = 'Interaction/Mutation_list.html',
        paginate_by = 50
    )

    return response

def mutation_search(request):


    if request.method == 'POST':

        form = MutationSearch(request.POST)
        if form.is_valid():

            handle = StringIO(form.cleaned_data['lines'])
            headers = handle.next().strip().split(',')
            print headers[0]
            req = set(['Entrez', 'Start', 'Stop'])
            extra_headers = list(set(headers) - req)
            good_lines = []
            for row in DictReader(handle, fieldnames = headers):


                valid_muts = Mutation.objects.filter(Position__gte = int(row['Start']))
                valid_muts = valid_muts.filter(Position__lte = int(row['Stop']))

                if form.cleaned_data['allow']:
                    valid_muts = valid_muts.filter(Q(Gene__Entrez = int(row['Entrez'])) or Q(Gene__isnull = True))
                else:
                    valid_muts = valid_muts.filter(Gene__Entrez = int(row['Entrez']))
                if valid_muts.exists():
                    try:
                        gene = Gene.objects.get(Entrez = int(row['Entrez']))
                    except MultipleObjectsReturned:
                        gene = Gene.objects.filter(Entrez = int(row['Entrez']))[0]



                    good_lines.append({'Gene':gene, 'labels':dict(map(lambda x: (x,row[x]), extra_headers)),
                                       'Position':(row['Start'], row['Stop']),
                                        'Mutations':valid_muts})

            context = {
                'form':form,
                'good_lines':good_lines,
                'extra_headers':extra_headers

            }
            if form.cleaned_data['csv_format']:
                return render_to_response('Interaction/mutation_results.csv', context,
                                          context_instance = RequestContext(request),
                                          mimetype='application/csv')
            else:
                return render_to_response('Interaction/mutation_search.html', context,
                                          context_instance = RequestContext(request))
    else:
        form = MutationSearch()


    context = {
        'form':form
    }    

    return render_to_response('Interaction/mutation_search.html', context,
                                context_instance = RequestContext(request))

