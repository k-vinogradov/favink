"""Main finite automata module."""

from types import MethodType


class InvalidTransition(RuntimeError):
    """
    Invalid Transition Exception.

    Exception is raised by FiniteAutomata instance is disallowed
    transition has been called.
    """


class AbortTransition(RuntimeError):
    pass


class FiniteAutomata:
    """
    Finite Automata Main Class (Mix-In).
    """

    transitions = dict()
    init_state = "init"

    def __init__(self):
        self._fa_allowed_cache = {}
        self._fa_state = self.init_state
        for transition in self.transitions:
            self._fa_add_action(transition)

    def get_state(self):
        """
        Get current state.

        Returns:
            str -- current state name
        """
        return self._fa_state

    def get_allowed_transitions(self):
        """
        Get allowed transition list for the current state.

        Returns:
            list -- allowed transitions
        """
        return self._fa_get_allowed()

    def is_allowed(self, transition):
        """
        Check if the transition is allowed for the current state.

        Arguments:
            transition {str} -- transition name

        Returns:
            bool -- True if the transition is allowed, otherwise is False
        """
        return transition in self._fa_get_allowed()

    def _fa_add_action(self, name):
        func = lambda self, *args, **kwargs: self._fa_do((name, args, kwargs))
        setattr(self, name, MethodType(func, self))

    def _fa_get_allowed(self):
        try:
            return self._fa_allowed_cache[self._fa_state]
        except KeyError:
            transitions = set()
            state = self._fa_state
            for transition, [origin, _] in self.transitions.items():
                if isinstance(origin, str):
                    origin = [origin]
                if state in origin:
                    transitions.add(transition)
            self._fa_allowed_cache[state] = transitions
            return transitions

    def _fa_do(self, transition_detail):
        name, args, kwargs = transition_detail
        if name not in self._fa_get_allowed():
            message = "Transition '{}' isn't allowed for state '{}'".format(
                name, self._fa_state
            )
            raise InvalidTransition(message)
        origin = self._fa_state
        target = self.transitions[name][1]

        self._fa_call_event_handler("after_{}".format(origin), name, *args, **kwargs)
        self._fa_call_event_handler("before_{}".format(target), name, *args, **kwargs)

        self._fa_state = target

        self._fa_call_event_handler(
            "on_{}".format(target), name, origin, *args, **kwargs
        )

    def _fa_call_event_handler(self, name, *args, **kwargs):
        try:
            getattr(self, name)(*args, **kwargs)
        except AttributeError:
            pass
