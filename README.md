# FAVink

[![Maintainability](https://api.codeclimate.com/v1/badges/7134fd6ab3adcd626ac9/maintainability)](https://codeclimate.com/github/k-vinogradov/favink/maintainability)
[![CodeFactor](https://www.codefactor.io/repository/github/k-vinogradov/favink/badge)](https://www.codefactor.io/repository/github/k-vinogradov/favink)
[![Build Status](https://travis-ci.org/k-vinogradov/favink.svg?branch=master)](https://travis-ci.org/k-vinogradov/favink)

Over-simple python finite automata (finite-state machine) implementation

## Getting Started

To install favink use the package from the PyPI repository:

    pip install favink

To add finite automata feature to the class in your code you have
to inherit FiniteAutomata class and define the following members:

- transitions table `transitions`
- initial state `init_state`
- event handlers methods.

### Transition Table and Initial State

The `transitions` is a dictionary where keys are transition names,
and values define the allowed and target states:

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

Initial state os defined by `init_state` member.

### Event Handlers

Each transition invokes the following events:

- `before`
- `on`
- `after`

To add event handler implement method `{before|on|after}_{state name}`.

#### `before_state_name(self, transition)`

Method is invoked __before__ the instance has been moved to the state
`state_name` because of transition has been called. Method argument:
`transition` - _string_, current transition name.

#### `on_state_name(self, transition, prevision_state)`

Method is invoked after the instance has been moved to the state `state_name`
because of transaction has been called. Method argument: `transition` - _string_,
current transition name, `prevision_state` - _string_, state before the transition
has been called.

#### `after_state_name(self, transition)`

Method is invoked before the instance has been moved out from the state.
Method argument: `transition` - _string_, current transition name.