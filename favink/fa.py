"""Main finite automata module."""

from types import MethodType


class InvalidTransition(RuntimeError):
    """
    Invalid Transition Exception.

    Exception is raised by FiniteAutomata instance is disallowed
    transition has been called.
    """


class FiniteAutomata:
    """
    Finite Automata Main Class (Mix-In).
    """

    # TODO: Detailed class description has to be added

    transitions = dict()
    init_state = "init"

    def __init__(self):
        self._fa_states_map = {}
        for transition, states in self.transitions.items():
            origin_states, _ = states
            self._fa_add_transition(transition, origin_states)
        self._fa_state = self.init_state

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
        return self._fa_states_map[self._fa_state]["transitions"]

    def is_allowed(self, transition):
        """
        Check if the transition is allowed for the current state.

        Arguments:
            transition {str} -- transition name

        Returns:
            bool -- True if the transition is allowed, otherwise is False
        """
        return transition in self.get_allowed_transitions()

    def _fa_add_state_to_map(self, transition, state):
        if state not in self._fa_states_map:
            self._fa_states_map[state] = {"transitions": [transition]}
            return
        self._fa_states_map[state]["transitions"].append(transition)

    def _fa_add_transition(self, transition, origin_states):
        if isinstance(origin_states, str):
            self._fa_add_state_to_map(transition, origin_states)
        else:
            for state in origin_states:
                self._fa_add_state_to_map(transition, state)
        make_transition = MethodType(
            lambda self: self._fa_make_transition(transition), self
        )
        setattr(self, transition, make_transition)

    def _fa_make_transition(self, transition):
        if not self.is_allowed(transition):
            error = (
                f"Transition '{transition}' isn't allowed for state {self.get_state()}"
            )
            raise InvalidTransition(error)

        previous_state = self.get_state()
        target = self.transitions[transition][1]

        self._fa_call_listener(f"after_{previous_state}", transition)
        self._fa_call_listener(f"before_{target}", transition)

        self._fa_state = target

        self._fa_call_listener(f"on_{target}", transition, previous_state)

    def _fa_call_listener(self, name, *args, **kwargs):
        listener = getattr(self, name, None)
        if not listener:
            return
        listener(*args, **kwargs)
