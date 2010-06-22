from django.conf.urls.defaults import *


urlpatterns = patterns('',
    # Example:
    # (r'^DistAnnot/', include('DistAnnot.foo.urls')),

    url(r'LabelMutation.html', 'Annot.views.LabelMutation', name = 'LabelMutation'),

)
