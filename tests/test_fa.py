"""Main FA test set."""
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
    """Test FA states changing."""
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
        assert simple_fa.get_state() == expected_state, f"Invalid state"


def test_allowed_transitions(simple_fa):
    """Test transition for allowed/disallowed status."""
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
    """Test for expections raising."""
    with pytest.raises(InvalidTransition):
        assert (
            simple_fa.move_to_d()
        ), "InvalidTransition exception is expected to be raised"
