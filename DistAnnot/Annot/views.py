# Create your views here.

from DistAnnot.Interaction.models import *
from DistAnnot.Annot.models import *

from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify

from forms import AnnotForm, InteractionEffectForm
from django.db.models import Count

from random import randint


@login_required
def LabelMutation(request, SentID = None, MutID = None):
    """A view to display the Mutation and sentence for annotation"""
    
    InteractionEffectFormset = formset_factory(InteractionEffectForm, extra = 0)
    
    if request.method == 'POST':
        annot_form = AnnotForm(request.POST, prefix = 'annot')
        effect_form = InteractionEffectFormset(request.POST, prefix = 'effect')
        sentence = Sentence.objects.get(id=int(request.POST['annot-SentenceID']))
        print request.POST['annot-MutID']
        mut = Mutation.objects.get(id=int(request.POST['annot-MutID']))
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

                    ie, isnew = InteractionEffect.objects.get_or_create(Interaction = inter,
                                                                        Mutation = mut,
                                                                        EffectType = effect)
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
            sentence = Sentence.objects.get(SentID)
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

    q = Sentence.objects.annotate(num_gene = Count('Mutation__Gene')).filter(num_gene__neq = 0)
    num_free = q.count()
    if num_free > 0:
        rind = randint(0, num_free)
    else:
        q = Sentence.objects.all()
        rind = randint(0, q.count())

    return q[rind]