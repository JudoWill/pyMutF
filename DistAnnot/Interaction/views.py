from django.shortcuts import render_to_response, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import list_detail
from django.views.decorators.cache import cache_page, never_cache
from csv import DictReader, DictWriter
from StringIO import StringIO
from DistAnnot.Interaction.models import *
from DistAnnot.Annot.models import *
from DistAnnot.Queries.models import *
from DistAnnot.Interaction.forms import *
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.template.defaultfilters import slugify
from django.template.defaultfilters import slugify


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
        paginate_by = 500
    )

    return response


def TagMutation(request, object_id = None):
    print object_id
    mut = get_object_or_404(Mutation, pk = int(object_id))
    TagFormset = formset_factory(MutationTagForm, can_delete = False, extra = 0)

    if request.method == 'POST':
        formset = TagFormset(request.POST)
        if formset.is_valid():
            print 'is valid'
            for form in formset.forms:
                tags = form.cleaned_data['Tags']
                print 'outside:', len(tags)
                art = Article.objects.get(pk = form.cleaned_data['Article'])
                for tag in tags:
                    try:
                        obj, isnew = Reference.objects.get_or_create(Article = art,
                                                                    Mutation = mut,
                                                                    Tag = tag)
                    except MultipleObjectsReturned:
                        continue
            return HttpResponseRedirect(reverse('mutation_detail', kwargs = {'object_id':mut.pk}))
        else:
            print 'not valid!!'
            articles = mut.GetArticles()

    else:
        initial = []
        articles = mut.GetArticles()
        for art in articles:
            initial.append({'Article':art.pk})
        formset = TagFormset(initial = initial)
    
    context_dict = {
        'formset':formset,
        'object':mut,
        'art_forms':zip(articles, formset.forms),
    }

    return render_to_response('Interaction/tag_mutation.html', context_dict,
                              context_instance = RequestContext(request))






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
                resp = HttpResponse()
                resp['Content-Disposition'] = 'attachment; filename=mutation_results.csv'
                MakeCSV(good_lines, resp)
                return resp
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

def MakeCSV(good_lines, response_obj):
	
	line_dicts = []
	field_names = line.labels.keys() + ['Start-Pos', 'End-Pos', 'Gene-Name', 'Mutation',
										'Effect-Type', 'HIVGene', 'Interaction-Type',
										'HumanGene', 'Articles']
	writer = DictWriter(response_obj, field_names)
	for line in good_lines:
		for mut in line.Mutations:
			val_dict = dict(line.labels.items())
			val_dict['Start-Pos'] = line.Positions[0]
			val_dict['End-Pos'] = line.Postions[1]
			val_dict['Gene-Name'] = line.Gene.Name or 'Unlabeled'
			val_dict['Mutation'] = mut.Mut
			val_dict['Effect-Type'] = mut.GetEffect.EffectType.Slug
			val_dict['HIVGene'] = mut.Interaction.latest.HIVGene.Name
			val_dict['Interaction-Type'] = mut.Interaction.latest.InteractionType.Type
			val_dict['HumanGene'] = mut.Interaction.latest.HumanGene.Name
			val_dict['Articles'] = '|'.join(map(lambda x: x.PMID, mut.GetArticles()))
			writer.writerow(val_dict)
		
			
	
	
	
	
