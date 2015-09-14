# -*- coding: utf-8 -*-
"""Urls"""

from django_states.views import make_state_transition

from .compat import patterns, url

urlpatterns = patterns('',
    url(r'^make-state-transition/$', make_state_transition, name='django_states_make_transition'),
)
