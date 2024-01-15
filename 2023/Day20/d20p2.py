import sys
import re
from collections import deque, Counter
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    from typing import Protocol

    # Setup data structures
    modules: dict[Module] = {}
    signal: tuple[str, bool, str]           #(to_module, signal, from_module)
    signalq: deque[signal] = deque()
    c = Counter()

    # Catalog all modules
    for line in lines:
        if line[0] == '%':
            module_type = FlipFlop
            line = line[1:]
        elif line[0] == '&':
            module_type = Conjunction
            line = line[1:]
        else:
            module_type = Broadcast
        name, output_modules = line.split(' -> ')

        modules[name] = module_type(name, output_modules.split(', '))

    # Record all input nodes
    for outputting_module in modules.values():
        for receiving_module in outputting_module.output_modules:
            if receiving_module not in modules:
                continue
            modules[receiving_module].input_modules[outputting_module.name] = False

    # Main loop 232605773145467
    run = True
    button_signal = ('broadcaster', False, None)
    i = 0
    while run:
        i += 1
        if check_default(modules):
            print("Default on i: ", i)
        if i % 100_000 == 0:
            print(i, "Default: ", check_default(modules))
            pprint(c)
        # Push button
        signalq.append(button_signal)

        # Process queue
        while signalq:
            # pprint(signalq)
            # Dequeue signal, keep track of count of signal types
            signal = signalq.popleft()

            if signal[0] == 'ls' and signal[1] == True:
                c.update(((signal[2], i),))
                check_module_default(modules[signal[2]])

            # print(signal)
            if signal[0] == 'rx' and signal[1] == False:
                print(f"rx: {signal[1]} i: {i}")
                run = False
                break
            # Process signal
            if signal[0] not in modules:
                continue
            new_signals = modules[signal[0]].process_signal(signal)
            for new_signal in new_signals:
                signalq.append(new_signal)

    # pprint(signalq)
    print(f"Min at {i=}")
    # answer = 232605773145467 multiplying the number of button presses each
    # for the 4 modules inputting into 'ls' (3,779×3,889×3,907×4,051)


class Module():
    signal: tuple[str, bool, str] = tuple()
    signals: list[signal] = []

    def __init__(
            self,
            name: str,
            output_modules: list[str]
            ) -> None:
        self.name = name
        self.output_modules = output_modules
        self.input_modules = dict()
        self.state = False
        self.type: str


    def __str__(self) -> str:
        return f"{self.name} ({self.type}) -> {self.output_modules}"

    # @Protocol
    # def process_signal(self, signal: signal) -> signals:
    #     pass

    
class FlipFlop(Module):
    signal: tuple[str, bool, str] = tuple()
    signals: list[signal] = []
    

    def __init__(
            self,
            name: str,
            output_modules: list[str]
            ) -> None:
        super().__init__(name, output_modules)
        self.type = 'FlipFlop'

    def process_signal(self, signal: signal) -> signals:
        new_signals = []
        if signal[1] == True:
            return new_signals
        self.state = not self.state
        new_signals = [(module, self.state, self.name) for module in self.output_modules]
        return new_signals


class Conjunction(Module):
    signal: tuple[str, bool, str] = tuple()
    signals: list[signal] = []

    def __init__(
            self,
            name: str,
            output_modules: list[str]
            ) -> None:
        super().__init__(name, output_modules)
        self.type = 'Conjunction'

    def process_signal(self, signal: signal) -> signals:
        # Remember imput state of module
        self.input_modules[signal[2]] = signal[1]
        # Grab all input states, and update output state as inverse of AND
        input_states = [state for state in self.input_modules.values()]
        self.state = not all(input_states)
        # Generate all outgoing signals
        new_signals = [(module, self.state, self.name) for module in self.output_modules]
        return new_signals
    

class Broadcast(Module):
    signal: tuple[str, bool, str] = tuple()
    signals: list[signal] = []

    def __init__(
            self,
            name: str,
            output_modules: list[str]
            ) -> None:
        super().__init__(name, output_modules)
        self.type = 'Broadcast'

    def process_signal(self, signal: signal) -> signals:
        # Generate all outgoing signals
        self.state = signal[1]
        new_signals = [(module, self.state, self.name) for module in self.output_modules]
        return new_signals

def check_default(modules: dict) -> bool:
    for module in modules.values():
        if module.state == True:
            return False
        for input_state in module.input_modules.values():
            if input_state == True:
                return False
    return True

def check_module_default(module: Module) -> bool:
    if module.state == True:
        return False
    for input_state in module.input_modules.values():
        if input_state == True:
            return False
    return True

main(sys.argv)


