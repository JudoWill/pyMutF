# Create your views here.

from DistAnnot.Interaction.models import *
from DistAnnot.Annot.models import *

from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from forms import AnnotForm, InteractionEffectForm


@login_required
def LabelMutation(request, SentID = None, MutID = None):
    """A view to display the Mutation and sentence for annotation"""
    
    InteractionEffectFormset = formset_factory(InteractionEffectForm, extra = 1)
    
    if request.method == 'POST':
        annot_form = AnnotForm(request.POST, prefix = 'annot')
        effect_form = InteractionEffectFormset(request.POST, prefix = 'effect')
        sentence = Sentence.objects.get(id=int(request.POST['SentenceID']))
        mut = Mutation.objects.get(id=int(request.POST['MutID']))
        if annot_form.is_valid():
            if not annot_form.cleaned_data['Bad_extraction']:
                if annot_form.cleaned_data['MutatedGene']:
                    mut_annot = MutationAnnot(User = request.user, Mutation = mut,
                                          GeneChosen = annot_form.cleaned_data['MutatedGene'])
                    mut_annot.save()
                    mut_annot.update_link()
                else:
                    mut.delete()
                picked_genes = annot_form.cleaned_data['MentionedGenes']
                for gene in picked_genes.exclude(id__in = sentence.Genes.all()):
                    obj = GeneAnnotation(Sentence = sentence, Gene = gene)
                    obj.save()
                    sentence.Genes.add()
            else:
                sentence.delete()
                mut.delete()

            return HttpResponseRedirect(reverse('LabelMutation'))


    else:
        if SentID:
            sentence = Sentence.objects.get(SentID)
        else:
            sentence = Sentence.objects.all().order_by('?')[0]
        if MutID:
            mut = Mutation.objects.get(id = int(MutID))
        else:
            mut = sentence.Mutation.latest('Gene')

        annot_form = AnnotForm(initial = {'SentenceID':sentence.id,
                                    'MutID':mut.id}, prefix = 'annot')
        inters = sentence.Interactions.all().values('id', 'HIVGene', 'HumanGene',
                                                    'InteractionType')
        effect_form = InteractionEffectFormset(prefix = 'effect',
                            initial=inters)

    out_dict = {'MutAnnotForm':annot_form,
                'EffectForm':effect_form,
                'sentence': sentence, 
                'mut':mut}

    return render_to_response("Annot/LabelMutation.html", out_dict,
                              context_instance = RequestContext(request))
