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
    count = Counter()

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

    # Main loop
    number_of_button_pushes = 1_000
    button_signal = ('broadcaster', False, None)
    for _ in range(number_of_button_pushes):
        # Push button
        signalq.append(button_signal)

        # Process queue
        while signalq:
            # pprint(signalq)
            # Dequeue signal, keep track of count of signal types
            signal = signalq.popleft()
            # print(signal)
            count.update(signal[1:2])
            # Process signal
            if signal[0] not in modules:
                continue
            new_signals = modules[signal[0]].process_signal(signal)
            for new_signal in new_signals:
                signalq.append(new_signal)

    # pprint(signalq)
    results = tuple(count.values())
    print(count, results[0]*results[1])


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


main(sys.argv)


