# Create your views here.

from Interaction.models import Sentence

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from forms import MutationAnnotForm


@login_required
def LabelMutation(request):
    """A view to display the Mutation and sentence for annotation"""

    if request.method == 'POST':

        form = MutationAnnotForm(request.POST)
        if form.is_valid():
            mut = form.save(commit = False)
            mut.User = request.User
            mut.save()
            mut.update_link()
            return HttpResponseRedirect(reverse('LabelMutation'))

    form = MutationAnnotForm()

    sentence = Sentence.objects.all().order_by('?')[0]
    out_dict = {'MutAnnotForm':form, 'sentence': sentence}

    return render_to_response("Annot/LabelMutation.html", out_dict,
                              context_instance = RequestContext(request))
