import sys
import re
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Build list of workflows and parts
    workflow_pattern = re.compile(r"(?P<name>\w+)\{(?P<conditions>.+)\}")
    part_pattern = re.compile(r"\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)")
    condition_pattern = re.compile(r"(?P<cat>\w)(?P<operator>[<>])(?P<num>\d+):(?P<workflow>\w+)")

    workflows = {}
    parts: list[Part] = []
    accepted: list[Part] = []
    Part.condition_pattern: re.Pattern = condition_pattern

    for line in lines:
        if line == '':
            pass
        elif line[0] == '{':
            match = part_pattern.search(line)
            parts.append(Part(match['x'], match['m'], match['a'], match['s']))
        else:
            match = workflow_pattern.search(line)
            workflows[match['name']] = match['conditions']
    # pprint(workflows, sort_dicts=False)
    # for part in parts:
    #     print(part)


    # Run workflows on all parts
    while parts:
        conditions = workflows[parts[-1].workflow]
        workflow = parts[-1].run_workflow(conditions)
        if workflow == 'A':
            accepted.append(parts.pop())
        elif workflow == 'R':
            parts.pop()
        # else rerun the last part with the new workflow
            
    sum = 0
    for part in accepted:
        total_rating = part.total_rating
        sum += total_rating
        print(part, total_rating, sum)




class Part():
    condition_pattern: re.Pattern # 'cat', 'operator', 'num', 'workflow'

    def __init__(self, x: int, m: int, a: int, s: int) -> None:
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)
        self.workflow = 'in'

    @property
    def total_rating(self) -> int:
        return self.x + self.m + self.a + self.s
    
    def __str__(self) -> str:
        return f"{{x={self.x},m={self.m},a={self.a},s={self.s}}}"

    def run_workflow(self, conditions: str) -> str:
        steps = conditions.split(',')
        for step in steps:
            if ':' not in step:
                self.workflow = step
                return step
            
            match = self.condition_pattern.search(step)
            if match['operator'] == '>':
                if self.__getattribute__(match['cat']) > int(match['num']):
                    self.workflow = match['workflow']
                    return match['workflow']
                else:
                    continue
            elif match['operator'] == '<':
                if self.__getattribute__(match['cat']) < int(match['num']):
                    self.workflow = match['workflow']
                    return match['workflow']
                else:
                    continue
            else:
                raise ValueError(f"Unrecognized opeartor: ", match['operator'])
            


main(sys.argv)


