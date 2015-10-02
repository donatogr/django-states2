# -*- coding: utf-8 -*-
"""Declared Exceptions"""


class States2Exception(Exception):
    pass


# ==========[ Transition exceptions ]==========

class TransitionException(States2Exception):
    pass


class TransitionOnUnsavedObject(TransitionException):
    def __init__(self, instance):
        TransitionException.__init__(self, "Cannot run state transition on unsaved object '%s'. "
                "Please call save() on this object first." % instance)


class PermissionDenied(TransitionException):
    def __init__(self, instance, transition, user):
        if user.is_authenticated():
            username = user.get_full_name()
        else:
            username = 'AnonymousUser'
        TransitionException.__init__(self, "Permission for executing the state '%s' has be denied to %s."
                % (transition, username))


class UnknownTransition(TransitionException):
    def __init__(self, instance, transition):
        TransitionException.__init__(self, "Unknown transition '%s' on %s" %
                    (transition, instance.__class__.__name__))


class TransitionNotFound(TransitionException):
    def __init__(self, model, from_state, to_state, transition_name=None):
        if from_state is not None and to_state is not None:
            msg = "Transition from '%s' to '%s' on %s not found" % (from_state, to_state, model.__name__)
        else:
            msg = "Transition with name '%s' on %s not found" % (transition_name, model.__name__)
        TransitionException.__init__(self, msg)


class TransitionCannotStart(TransitionException):
    def __init__(self, instance, transition):
        TransitionException.__init__(self, "Transition '%s' on %s cannot start in the state '%s'" %
                    (transition, instance.__class__.__name__, instance.state))


class TransitionNotValidated(TransitionException):
    def __init__(self, instance, transition, validation_errors):
        TransitionException.__init__(self, "Transition '%s' on %s does not validate (%i errors)" %
                    (transition, instance.__class__.__name__, len(validation_errors)))
        self.validation_errors = validation_errors


class TransitionValidationError(TransitionException):
    """
    Errors yielded from StateTransition.validate.
    """
    pass

# ==========[ Definition exceptions ]==========

class DefinitionException(States2Exception):
    pass

class MachineDefinitionException(DefinitionException):
    def __init__(self, machine, description):
        DefinitionException.__init__(self, 'Error in state machine (%s) definition: %s' % (machine.__name__, description))

class StateDefinitionException(DefinitionException):
    def __init__(self, description):
        DefinitionException.__init__(self, 'Error in state definition: ' + description)

class GroupDefinitionException(DefinitionException):
    def __init__(self, description):
        DefinitionException.__init__(self, 'Error in state group definition: ' + description)

class TransitionDefinitionException(DefinitionException):
    def __init__(self, description):
        DefinitionException.__init__(self, 'Error in state transition definition: ' + description)


# ==========[ Other exceptions ]==========

class UnknownState(States2Exception):
    def __init__(self, state):
        States2Exception.__init__(self, 'State "%s" does not exist' % state)
