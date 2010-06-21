from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import Interaction.views
import Interaction.urls

urlpatterns = patterns('',
    # Example:
    # (r'^DistAnnot/', include('DistAnnot.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^index.html', 'Interaction.views.index'),
    (r'^interactions/', include('Interaction.urls'))
)
