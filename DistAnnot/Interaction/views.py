from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.conf import settings
# Create your views here.



def index(request):

    return render_to_response('index.html')