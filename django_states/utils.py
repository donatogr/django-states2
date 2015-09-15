# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def graph_elements_for_model(model_class, field_name):
    machine = getattr(model_class(), 'get_%s_machine' % field_name)()
    name = str(model_class._meta.verbose_name)
    return graph_elements(name, machine)


def graph_elements(name, machine):
    graph = {'nodes': [], 'edges': []}

    for state in list(machine.states.keys()):
        graph['nodes'].append({'data': {'id': state, 'name': state}})

    for trion_name, trion in machine.transitions.iteritems():
        for from_state in trion.from_states:
            graph['edges'].append(
                {'data': {
                    'id': '%s_%s_%s' % (trion_name, from_state, trion.to_state),
                    'name': trion_name,
                    'source': from_state,
                    'target': trion.to_state
                }}
            )
    return graph
