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

    def __init__(self):
        FiniteAutomata.__init__(self)
        self.journal = []

    def add_journal_item(self, event, target, transition, previous_state=None):
        """Add new record to the instance's journal."""
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
        """Handle state-changing-event."""
        self.add_journal_item("after", "init", transition)

    def before_init(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("before", "init", transition)

    def on_init(self, transition, previous_state):
        """Handle state-changing-event."""
        self.add_journal_item("on", "init", transition, previous_state)

    def after_a(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("after", "a", transition)

    def before_a(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("before", "a", transition)

    def on_a(self, transition, previous_state):
        """Handle state-changing-event."""
        self.add_journal_item("on", "a", transition, previous_state)

    def after_b(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("after", "b", transition)

    def before_b(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("before", "b", transition)

    def on_b(self, transition, previous_state):
        """Handle state-changing-event."""
        self.add_journal_item("on", "b", transition, previous_state)

    def after_c(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("after", "c", transition)

    def before_c(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("before", "c", transition)

    def on_c(self, transition, previous_state):
        """Handle state-changing-event."""
        self.add_journal_item("on", "c", transition, previous_state)

    def after_d(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("after", "d", transition)

    def before_d(self, transition):
        """Handle state-changing-event."""
        self.add_journal_item("before", "d", transition)

    def on_d(self, transition, previous_state):
        """Handle state-changing-event."""
        self.add_journal_item("on", "d", transition, previous_state)


class Car(FiniteAutomata):
    """README example."""

    init_state = "stopped"
    transitions = {
        "start_engine": ["stopped", "idle"],
        "stop_engine": ["idle", "stopped"],
        "forward": ["idle", "moving_forward"],
        "backward": ["idle", "moving_backward"],
        "stop": [["moving_forward", "moving_backward"], "idle"],
    }

    def on_stopped(self, *_):
        print("Engine has been stopped")

    def on_idle(self, *_):
        print("I'm not moving, but engine is on")

    def on_moving_forward(self, *_):
        print("Let's go!")

    def on_moving_backward(self, *_):
        print("Why are we retreating?")


@pytest.fixture()
def simple_fa():
    """Get simple state machine instance."""
    return SimpleFA()


@pytest.fixture()
def car():
    """Get state machine to test README example"""
    return Car()
