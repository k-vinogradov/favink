"""Test to be sure that examples from README work."""

import pytest

from favink import InvalidTransition


def test_output(car, capfd):
    """Test the example's output."""
    car.start_engine()
    car.forward()
    car.stop()
    car.backward()
    car.stop()
    car.stop_engine()
    output, _ = capfd.readouterr()
    assert (
        output == "I'm not moving, but engine is on\n"
        "Let's go!\n"
        "I'm not moving, but engine is on\n"
        "Why are we retreating?\n"
        "I'm not moving, but engine is on\n"
        "Engine has been stopped\n"
    )


def test_exception(car):
    """Test that example raises the exception."""
    car.start_engine()
    car.forward()
    with pytest.raises(InvalidTransition):
        car.stop_engine()
