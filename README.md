# FAVink

[![Maintainability](https://api.codeclimate.com/v1/badges/7134fd6ab3adcd626ac9/maintainability)](https://codeclimate.com/github/k-vinogradov/favink/maintainability)
[![CodeFactor](https://www.codefactor.io/repository/github/k-vinogradov/favink/badge)](https://www.codefactor.io/repository/github/k-vinogradov/favink)
[![Build Status](https://travis-ci.org/k-vinogradov/favink.svg?branch=master)](https://travis-ci.org/k-vinogradov/favink)

- [FAVink](#favink)
  - [Getting Started](#getting-started)
  - [Transition Table and Initial State](#transition-table-and-initial-state)
  - [Events](#events)
    - [Event Handler Definitions](#event-handler-definitions)
  - [Car Example](#car-example)
  - [API Reference](#api-reference)
    - [Predefined `FiniteAutomata` Methods](#predefined-finiteautomata-methods)
      - [`FiniteAutomata.get_state(self)`](#finiteautomatagetstateself)
      - [`FiniteAutomata.get_allowed_transitions(self)`](#finiteautomatagetallowedtransitionsself)
      - [`FiniteAutomata.is_allowed(self, transition)`](#finiteautomataisallowedself-transition)
    - [Transition Methods](#transition-methods)

Over-simple python finite automata (finite-state machine) implementation

## Getting Started

To install favink use the package from the PyPI repository:

    pip install favink

To add finite automata feature to the class in your code you have to inherit
FiniteAutomata class and define the following members:

- transitions table `transitions`
- initial state `init_state`
- event handlers methods.

For every transition the constructor creates a dynamic method with argument mask
(`self, **args, **kwargs`). Each method is named after the transition.

To make the transition you should call the transition method. After the method
has been called it changes the instance state and invoke related event handlers.
If the called transition isn't allowed for the current state `InvalidTransition`
extension will be raised.****

## Transition Table and Initial State

The `transitions` is a dictionary where keys are transition names,
values define the allowed and target states:

```Python
transitions = {
    "transition_1":
    [
        "allowed_state_1",
        "target_state_1"
    ],
    "transition_2":
    [
        [
            "allowed_state_2",
            "allowed_state_3"
        ],
        "target_state_2"
    ]
}
```

Initial state is defined by `init_state` member.

## Events

![Transition Life Cycle](https://github.com/k-vinogradov/favink/raw/master/docs/images/lifecycle.svg?sanitize=true)

Making of transition triggers the following events and invokes the related handlers
(if they have been implemented in the class):

- `after`
- `before`
- `on`

### Event Handler Definitions

For every state (for example `state_name`) the following methods can be defined:

```Python
def before_state_name(self, transition_detail):
    ...


def on_state_name(self, transition_detail, origin_state):
    ...


def after_state_name(self, transition_detail):
    ...
```

Transition detail is a 3-item tuple `(name, args, kwargs)` where

- `name` is a transition name;
- `args` is a list contains the positional arguments passed to the transition call,
- `kwargs` is a dictionary with keyword arguments passed to the transition call,

If `after_...` or `before...` handlers raise the exception transition is aborted.

## Car Example

![Transition Life Cycle](https://github.com/k-vinogradov/favink/raw/master/docs/images/car.svg?sanitize=true)

```Python
class Car(FiniteAutomata):
    init_state = "stopped"
    transitions = {
        "start_engine": ["stopped", "idle"],
        "stop_engine": ["idle", "stopped"],
        "forward": ["idle", "moving_forward"],
        "backward": ["idle", "moving_backward"],
        "stop": [["moving_forward", "moving_backward"], "idle"],
    }

    def on_stopped(self, transition, origin):
        print("Engine has been stopped")

    def on_idle(self, transition, origin):
        print("I'm not moving, but engine is on")

    def on_moving_forward(self, transition, origin):
        print("Let's go!")

    def on_moving_backward(self, transition, origin):
        print("Why are we retreating?")

car = Car()

car.start_engine()
car.forward()
car.stop()
car.backward()
car.stop()
car.stop_engine()
```

Output:

    I'm not moving, but engine is on
    Let's go!
    I'm not moving, but engine is on
    Why are we retreating?
    I'm not moving, but engine is on
    Engine has been stopped

## API Reference

### Predefined `FiniteAutomata` Methods

#### `FiniteAutomata.get_state(self)`

Returns the current instance state name as a string.

#### `FiniteAutomata.get_allowed_transitions(self)`

Return the list contains all transactions which are allowed for the current instance state.

#### `FiniteAutomata.is_allowed(self, transition)`

### Transition Methods

Dynamically defined methods for every transition (key) in the `transitions` dictionary.