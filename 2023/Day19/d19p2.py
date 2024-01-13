from copy import copy

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

    # Build list of workflows
    workflow_pattern = re.compile(r"(?P<name>\w+)\{(?P<conditions>.+)\}")
    condition_pattern = re.compile(r"(?P<cat>\w)(?P<operator>[<>])(?P<num>\d+):(?P<workflow>\w+)")

    workflows = {}
    for line in lines:
        if line == '':
            continue
        elif line[0] == '{':
            continue
        else:
            match = workflow_pattern.search(line)
            workflows[match['name']] = match['conditions']
    # pprint(workflows, sort_dicts=False)

    # Initialize
    ranges: list[Range] = []
    accepted: list[Range] = []
    Range.ranges: list[Range] = ranges
    Range.condition_pattern: re.Pattern = condition_pattern

    ranges.append(Range(x_range=(1, 4000),
                        m_range=(1, 4000),
                        a_range=(1, 4000),
                        s_range=(1, 4000)))

    # Run workflows on all parts
    while ranges:
        range = ranges.pop()
        if range.workflow == 'A':
            accepted.append(range)
            continue
        elif range.workflow == 'R':
            continue
        conditions = workflows[range.workflow]
        range.run_workflow(conditions)
            
    sum = 0
    for range in accepted:
        combinations = range.combinations
        sum += combinations
        print(range, combinations, sum)



class Range():
    ranges: list["Range"]
    condition_pattern: re.Pattern

    def __init__(
            self,
            x_range: tuple[int],
            m_range: tuple[int],
            a_range: tuple[int],
            s_range: tuple[int]
            ) -> None:
        self.x = x_range
        self.m = m_range
        self.a = a_range
        self.s = s_range
        self.workflow = 'in'

    @property
    def combinations(self) -> int:
        x = self.x[1] - self.x[0] + 1
        m = self.m[1] - self.m[0] + 1
        a = self.a[1] - self.a[0] + 1
        s = self.s[1] - self.s[0] + 1
        return x * m * a * s
    
    def __str__(self) -> str:
        return f"x{self.x},m{self.m},a{self.a},s{self.s}"

    def run_workflow(self, conditions: str) -> None:
        # eg. rfg{s<537:gd,x>2440:R,A}
        # 'cat', 'operator', 'num', 'workflow'
        conditions = conditions.split(',')
        for condition in conditions:
            if ':' not in condition:
                self.workflow = condition
                self.ranges.append(self)
                return
            
            match = self.condition_pattern.search(condition)
            cond_category = match['cat']
            category_range = self.__getattribute__(cond_category)
            cond_opreator = match['operator']
            cond_number = int(match['num'])
            cond_new_workflow = match['workflow']

            if cond_opreator == '>':
                if category_range[1] > cond_number:
                    # Split range into 2
                    new_range = copy(self)
                    new_range.__setattr__(cond_category, (cond_number+1, category_range[1]))
                    new_range.workflow = cond_new_workflow
                    self.ranges.append(new_range)
                    # Reduce original range
                    self.__setattr__(cond_category, (category_range[0], cond_number))
                else:
                    # Condition not cover range, skip
                    continue
            elif cond_opreator == '<':
                if category_range[0] < cond_number:
                    # Split range into 2
                    new_range = copy(self)
                    new_range.__setattr__(cond_category, (category_range[0], cond_number-1))
                    new_range.workflow = cond_new_workflow
                    self.ranges.append(new_range)
                    # Reduce original range
                    self.__setattr__(cond_category, (cond_number, category_range[1]))
                else:
                    # Condition not cover range, skip
                    continue
            else:
                raise ValueError(f"Unrecognized opeartor: ", cond_opreator)
            


main(sys.argv)


