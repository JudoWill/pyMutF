# Create your views here.

from DistAnnot.Interaction.models import *
from DistAnnot.Annot.models import *

from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.db import IntegrityError
from django.views.decorators.cache import never_cache, cache_page
from django.utils import simplejson

from forms import AnnotForm, InteractionEffectForm
from django.db.models import Count

from random import randint
from DistAnnot.CreateOrder import UpdatePriority

@never_cache
@login_required
def LabelMutation(request, SentID = None, MutID = None):
    """A view to display the Mutation and sentence for annotation"""
    print str(SentID), str(MutID)
    if not SentID is None:
        SentID = int(SentID)
    if not MutID is None:
        MutID = int(MutID)
        
    InteractionEffectFormset = formset_factory(InteractionEffectForm, extra = 0)
    
    if request.method == 'POST':
        annot_form = AnnotForm(request.POST, prefix = 'annot')
        effect_form = InteractionEffectFormset(request.POST, prefix = 'effect')
        sentence = Sentence.objects.get(id=int(request.POST['annot-SentenceID']))
        print request.POST['annot-MutID']
        try:
            mut = Mutation.objects.get(id=int(request.POST['annot-MutID']))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('LabelMutation'))



        if annot_form.is_valid() and effect_form.is_valid():
            if not annot_form.cleaned_data['Bad_extraction']:
                if annot_form.cleaned_data['MutatedGene']:
                    mut_annot = MutationAnnot(User = request.user, Mutation = mut,
                                          GeneChosen = annot_form.cleaned_data['MutatedGene'])
                    mut_annot.save()
                    mut_annot.update_link()
                    mut.Gene = annot_form.cleaned_data['MutatedGene']
                    mut.save()
                    #Send a message
                    request.user.message_set.create(message = 'Sucessfully attributed %s to %s' % (str(mut), str(mut_annot.GeneChosen)))
                else:
                    #Send a message
                    request.user.message_set.create(message = 'Sucessfully deleted %s' % str(mut))

                    mut.delete()

                #update the priority based on the new mutation information
                UpdatePriority(sentence)

                picked_genes = annot_form.cleaned_data['MentionedGenes']
                if picked_genes:
                    for gene in picked_genes.exclude(id__in = sentence.Genes.all()):
                        obj = GeneAnnotation(Sentence = sentence, Gene = gene)
                        obj.save()
                        #sentence.Genes.add(obj)
                        GeneAnnot(User = request.user, Annotation = obj).save()

                        #Send a message
                        request.user.message_set.create(message = 'Sucessfully added %s ' % str(gene))

                for eform in effect_form.forms:
                    inter = Interaction.objects.get(id = eform.cleaned_data['id'])
                    if len(eform.cleaned_data['EffectFreeText']) > 0:
                        txt = eform.cleaned_data['EffectFreeText']
                        effect, isnew = EffectType.objects.get_or_create(Slug = slugify(txt),
                                                                             Description = txt)
                        if isnew:
                            #Send a message
                            request.user.message_set.create(message = 'Sucessfully created %s ' % str(effect.Slug))

                    elif not eform.cleaned_data['EffectChoice'] is None:
                        effect = eform.cleaned_data['EffectChoice']
                    else:
                        continue
                    try:
                        ie, isnew = InteractionEffect.objects.get_or_create(Interaction = inter,
                                                                            Mutation = mut,
                                                                            EffectType = effect)
                    except IntegrityError:
                        continue

                    if isnew:
                        InteractionEffectAnnot(User = request.user, InteractionEffect = ie,
                                               EffectChosen = effect).save()
                        #Send a message
                        txt = 'Sucessfully annotated intection effect %s to %s' % (str(effect.Slug), str(mut))
                        request.user.message_set.create(message = txt)




            else:
                request.user.message_set.create(message = 'Sucessfully deleted the jiberish sentence.')
                sentence.delete()
                mut.delete()

            return HttpResponseRedirect(reverse('LabelMutation'))
        else:
            inters = sentence.Article.Interactions.all().values('id')
            zipped_inter_forms = zip(effect_form.forms, sentence.Article.Interactions.all())

    else:
        if SentID:
            sentence = Sentence.objects.get(id = SentID)
        else:
            sentence = GetRandomSent()
        if MutID:
            mut = Mutation.objects.get(id = int(MutID))
        else:
            mut = sentence.Mutation.latest('Gene')

        annot_form = AnnotForm(initial = {'SentenceID':sentence.id,
                                    'MutID':mut.id}, prefix = 'annot')

        inters = sentence.Article.Interactions.all().values('id')
        effect_form = InteractionEffectFormset(prefix = 'effect', 
                                                initial = inters)
        zipped_inter_forms = zip(effect_form.forms, sentence.Article.Interactions.all())

    article = sentence.Article
    out_dict = {'MutAnnotForm':annot_form,
                'EffectForm':effect_form,
                'sentence': sentence, 
                'mut':mut,
                'interactions':inters,
                'zipped_forms': zipped_inter_forms,
                'Article':article,
                'PrevActions':request.user.get_and_delete_messages()}

    return render_to_response("Annot/LabelMutation.html", out_dict,
                              context_instance = RequestContext(request))


def GetRandomSent():

    q = Sentence.objects.filter(Priority__isnull = False).order_by('Priority', 'RandOrder')
    num_free = q.count()
    if num_free > 0:
        rind = 0
    else:
        q = Sentence.objects.all()
        rind = randint(0, q.count())

    sent = q[rind]
    UpdatePriority(sent)

    return sent


#@cache_page(60 * 60)
def gene_list(request, q = None):

    def MakeList(gene_qset, extra_qset):
        tlist = []
        for item in gene_qset:
            tlist.append('GN:'+item)
        for item in extra_qset:
            tlist.append('ON:'+item)
        return tlist

    print request.GET
    ids = request.GET.get('q', None)
    print ids
    gene_query = Gene.objects.filter(Name__icontains = ids).values_list('Name', flat = True)
    extra_names = ExtraGeneName.objects.filter(Name__icontains = ids).values_list('Name', flat = True)
    print gene_query.count(), extra_names.count()
    l = MakeList(gene_query, extra_names)
    print l
    return HttpResponse(simplejson.dumps(l)[1:-1], mimetype='application/javascript')


def label_random(request):

    sent = GetRandomSent()
    mut = sent.Mutation.all()[0]

    return HttpResponseRedirect(reverse('mutation_tag', kwargs = {'object_id':mut.id}))

    