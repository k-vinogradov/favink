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
        setattr(self, name, MethodType(lambda self: self._fa_do(name), self))

    def _fa_get_allowed(self):
        state = self._fa_state

        if state in self._fa_allowed_cache:
            return self._fa_allowed_cache[state]
        transitions = set()

        for transition, states in self.transitions.items():
            origin, _ = states
            if (isinstance(origin, str) and origin == state) or state in origin:
                transitions.add(transition)

        self._fa_allowed_cache[state] = transitions
        return transitions

    def _fa_do(self, transition):
        if transition not in self._fa_get_allowed():
            raise InvalidTransition(
                f"Transition '{transition}' isn't allowed for state {self._fa_state}"
            )

        origin = self._fa_state
        target = self.transitions[transition][1]

        self._fa_call_event_handler(f"after_{origin}", transition)
        self._fa_call_event_handler(f"before_{target}", transition)

        self._fa_state = target

        self._fa_call_event_handler(f"on_{target}", transition, origin)

    def _fa_call_event_handler(self, name, *args, **kwargs):
        if hasattr(self, name):
            getattr(self, name)(*args, **kwargs)
