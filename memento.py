# memento.py
import payroll as pr


class Memento:
    def __init__(self, payroll=pr.Payroll):
        self.state = payroll

    def restore(self):
        return self.state


class CareTaker:
    def __init__(self, prev=list(), next_states=list()):
        self.previous_states = prev
        self.next_states = next_states

    def __str__(self):
        return "PREVIOUS STATES: {}\nNEXT STATES: {}\n".format(len(self.previous_states), len(self.next_states))

    def add_state(self, payroll):
        state = Memento(payroll)
        if self.next_states:
            self.next_states.clear()
        self.previous_states.append(state)

    def undo(self):
        last_state = self.previous_states.pop()
        self.next_states.append(last_state)

        new_payroll = last_state.restore()
        return new_payroll

    def redo(self):
        state = self.next_states.pop()
        self.previous_states.append(state)
        new_payroll = state.restore()
        return new_payroll
