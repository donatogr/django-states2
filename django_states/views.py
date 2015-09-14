# -*- coding: utf-8 -*-
"""Views"""
import json

from django.contrib.admindocs.views import ModelDetailView
from django.db.models import FieldDoesNotExist
from django.http import (Http404, HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe

from django_states.exceptions import PermissionDenied
from django_states.utils import graph_elements_for_model

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models import get_model


class StateMachineView(ModelDetailView):
    template_name = 'django_states/display_state_machine.html'

    def get_context_data(self, **kwargs):
        #context_data['field_name'] = kwargs['field_name']
        context_data = super(StateMachineView, self).get_context_data(**kwargs)
        context_data['graph_elements'] = get_state_machine_graph_elements(**context_data)
        return context_data


def get_state_machine_graph_elements(app_label, model_name, field_name, **kwargs):
    try:
        model_class = get_model(app_label, model_name)
    except LookupError:
        raise Http404

    try:
        field = model_class._meta.get_field(field_name)
    except FieldDoesNotExist:
        raise Http404

    data = graph_elements_for_model(model_class, field_name)
    return mark_safe(json.dumps(data))


def make_state_transition(request):
    """
    View to be called by AJAX code to do state transitions. This must be a
    ``POST`` request.

    Required parameters:

    - ``model_name``: the name of the state model, as retured by
      ``instance.get_state_model_name``.
    - ``action``: the name of the state transition, as given by
      ``StateTransition.get_name``.
    - ``id``: the ID of the instance on which the state transition is applied.

    When the handler requires additional kwargs, they can be passed through as
    optional parameters: ``kwarg-{{ kwargs_name }}``
    """
    if request.method == 'POST':
        # Process post parameters
        app_label, model_name = request.POST['model_name'].split('.')
        try:
            model = get_model(app_label, model_name)
        except LookupError:
            model = None
        instance = get_object_or_404(model, id=request.POST['id'])
        action = request.POST['action']

        # Build optional kwargs
        kwargs = {}
        for p in request.REQUEST:
            if p.startswith('kwarg-'):
                kwargs[p[len('kwargs-')-1:]] = request.REQUEST[p]

        if not hasattr(instance, 'make_transition'):
            raise Exception('No such state model "%s"' % model_name)

        try:
            # Make state transition
            instance.make_transition(action, request.user, **kwargs)
        except PermissionDenied, e:
            return HttpResponseForbidden()
        else:
            # ... Redirect to 'next'
            if 'next' in request.REQUEST:
                return HttpResponseRedirect(request.REQUEST['next'])
            else:
                return HttpResponse('OK')
    else:
        return HttpResponseForbidden()
