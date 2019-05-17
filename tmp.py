from favink import FiniteAutomata


class Car(FiniteAutomata):
    transitions = {
        "start_engine": ["stopped", "idle"],
        "start_driving": ["idle", "moving"],
        "stop_driving": ["moving", "idle"],
        "stop_engine": ["idle", "stopped"],
    }
    init_state = "stopped"

    def on_idle(self, _, prevision_state):
        print(prevision_state, "->", self.get_state())

    def after_stopped(self, _):
        print("Leaving the 'stopped' state")

    def before_stopped(self, _):
        print("Going to 'stopped'")


car = Car()
car.start_engine()
car.stop_engine()
