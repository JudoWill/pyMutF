from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:

import Interaction.views


urlpatterns = patterns('',
     (r'^index.html', 'Interaction.views.interaction_index')
)
