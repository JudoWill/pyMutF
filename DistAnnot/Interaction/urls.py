from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:




urlpatterns = patterns('',
     url(r'^stats.html', 'Interaction.views.stats', name = 'stats'),
)
