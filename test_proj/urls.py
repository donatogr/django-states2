from .compat import patterns, include, url

from django.contrib import admin
from django_states.views import StateMachineView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_proj.views.home', name='home'),
    # url(r'^test_proj/', include('test_proj.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/doc/models/(?P<app_label>[^>]+)>(?P<model_name>[^/]+)/(?P<field_name>[^/]+)/$', StateMachineView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
