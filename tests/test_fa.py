import pytest
from favink import InvalidTransition


def compare_lists(list_a, list_b):
    """Compare the content of tho lists regardless items order."""
    if len(list_a) != len(list_b):
        return False
    if not list_a:
        return True
    value, *new_a = list_a
    if value not in list_b:
        return False
    new_b = list(filter(lambda x: x != value, list_b))
    return compare_lists(new_a, new_b)


def test_states(simple_fa):
    assert simple_fa.get_state() == "init", "Invalid init state"
    actions = [
        ["move_from_init_to_a", "a"],
        ["move_from_a_to_b", "b"],
        ["move_to_d", "d"],
        ["move_from_d_to_a", "a"],
        ["move_to_d", "d"],
    ]
    for action, expected_state in actions:
        getattr(simple_fa, action)()
        assert simple_fa.get_state() == expected_state, "Invalid state"


def test_allowed_transitions(simple_fa):
    simple_fa.move_from_init_to_a()
    assert compare_lists(
        simple_fa.get_allowed_transitions(),
        ["move_to_d", "move_from_a_to_b", "move_from_a_to_c"],
    ), "Invalid allowed transition list"
    assert simple_fa.is_allowed("move_to_d"), "Transition is expected to be allowed"
    assert not simple_fa.is_allowed(
        "move_from_d_to_a"
    ), "Transition is expected to disallowed"


def test_exceptions(simple_fa):
    with pytest.raises(InvalidTransition):
        assert (
            simple_fa.move_to_d()
        ), "InvalidTransition exception is expected to be raised"


def test_events(simple_fa):
    assert not simple_fa.journal
    simple_fa.move_from_init_to_a("arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")
    assert len(simple_fa.journal) == 3
    assert simple_fa.journal[-3:] == [
        {
            "event": "after",
            "target": "init",
            "state": "init",
            "transition": "move_from_init_to_a",
            "previous_state": None,
            "args": ("arg1", "arg2"),
            "kwargs": {"kwarg1": "kwarg1", "kwarg2": "kwarg2"},
        },
        {
            "event": "before",
            "target": "a",
            "state": "init",
            "transition": "move_from_init_to_a",
            "previous_state": None,
            "args": ("arg1", "arg2"),
            "kwargs": {"kwarg1": "kwarg1", "kwarg2": "kwarg2"},
        },
        {
            "event": "on",
            "target": "a",
            "state": "a",
            "transition": "move_from_init_to_a",
            "previous_state": "init",
            "args": ("arg1", "arg2"),
            "kwargs": {"kwarg1": "kwarg1", "kwarg2": "kwarg2"},
        },
    ]
