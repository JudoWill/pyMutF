# Create your views here.

from DistAnnot.Interaction.models import *
from DistAnnot.Annot.models import *

from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from forms import AnnotForm


@login_required
def LabelMutation(request, SentID = None, MutID = None):
    """A view to display the Mutation and sentence for annotation"""

    if request.method == 'POST':
        form = AnnotForm(request.POST)
        sentence = Sentence.objects.get(id=int(request.POST['SentenceID']))
        mut = Mutation.objects.get(id=int(request.POST['MutID']))
        if form.is_valid():
            if not form.cleaned_data['Bad_extraction']:
                if form.cleaned_data['MutatedGene']:
                    mut_annot = MutationAnnot(User = request.user, Mutation = mut,
                                          GeneChosen = form.cleaned_data['MutatedGene'])
                    mut_annot.save()
                    mut_annot.update_link()
                else:
                    mut.delete()
                picked_genes = form.cleaned_data['MentionedGenes']
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

        form = AnnotForm(initial = {'SentenceID':sentence.id,
                                    'MutID':mut.id})

    out_dict = {'MutAnnotForm':form, 'sentence': sentence, 'mut':mut}

    return render_to_response("Annot/LabelMutation.html", out_dict,
                              context_instance = RequestContext(request))
