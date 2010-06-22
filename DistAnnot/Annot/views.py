# Create your views here.
from Interaction.models import *
from Annot.models import *

from django.utils.translation import ugettext as _
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext




@login_required
def LabelMutation(request, MutID = None):
    """A view to display the Mutation and sentence for annotation"""


    return render_to_response('Annot/LabelMutation.html', context_instance = RequestContext(request))
