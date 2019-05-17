"""Pytest fixtures."""

import pytest
from favink import FiniteAutomata


class SimpleFA(FiniteAutomata):
    """Simple state machine example."""

    transitions = {
        "move_from_init_to_a": ["init", "a"],
        "move_from_a_to_b": ["a", "b"],
        "move_from_a_to_c": ["a", "c"],
        "move_to_d": [["a", "b", "c"], "d"],
        "move_from_d_to_a": ["d", "a"],
    }
    journal = []

    def add_event(self, event, target, transition, previous_state=None):
        self.journal.append(
            {
                "event": event,
                "target": target,
                "state": self.get_state(),
                "transition": transition,
                "previous_state": previous_state,
            }
        )

    def after_init(self, transition):
        self.add_event("after", "init", transition)

    def before_init(self, transition):
        self.add_event("before", "init", transition)

    def on_init(self, transition, previous_state):
        self.add_event("on", "init", transition, previous_state)

    def after_a(self, transition):
        self.add_event("after", "a", transition)

    def before_a(self, transition):
        self.add_event("before", "a", transition)

    def on_a(self, transition, previous_state):
        self.add_event("on", "a", transition, previous_state)

    def after_b(self, transition):
        self.add_event("after", "b", transition)

    def before_b(self, transition):
        self.add_event("before", "b", transition)

    def on_b(self, transition, previous_state):
        self.add_event("on", "b", transition, previous_state)

    def after_c(self, transition):
        self.add_event("after", "c", transition)

    def before_c(self, transition):
        self.add_event("before", "c", transition)

    def on_c(self, transition, previous_state):
        self.add_event("on", "c", transition, previous_state)

    def after_d(self, transition):
        self.add_event("after", "d", transition)

    def before_d(self, transition):
        self.add_event("before", "d", transition)

    def on_d(self, transition, previous_state):
        self.add_event("on", "d", transition, previous_state)


@pytest.fixture()
def simple_fa():
    """Get simple state machine instance."""
    return SimpleFA()
