import sys
from pathlib import Path

# Run module via python3 -m d#p#, any argument passed uses puzzle data
# no argument passed uses test data 

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    hands: list[str] = []
    for line in lines:
        hands.append(Hand(line.split()[0], line.split()[1]))

    sorted_hands = sorted(hands)

    sum = 0
    for rank, hand in zip(range(1, len(hands) + 1), sorted_hands):
        sum += rank*hand.bid
        print(rank, hand, rank*hand.bid, sum)

class Hand():
    def __init__(self, cards: str, bid: int) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.type = self.get_type()

    def get_type(self) -> int:
        if len(self.cards) != 5:
            raise ValueError(f"Hand ({self.cards}) is not 5 chars")
        # Types
        # 7) 5 of kind
        # 6) 4 of a kind
        # 5) full house
        # 4) three of a kind
        # 3) two pair
        # 2) one pair
        # 1) high card
        jokers = 0       
        counter = {}
        for card in self.cards:
            if card == 'J':
                jokers += 1
            else:
                counter[card] = counter.get(card, 0) + 1

        if len(counter.keys()) == 0:
            return 7
        if len(counter.keys()) == 1:
            return 7
        if len(counter.keys()) == 2:
            if max(counter.values()) + jokers == 4:
                return 6
            else:
                return 5
        if len(counter.keys()) == 3:
            if max(counter.values()) +  jokers == 3:
                return 4
            else:
                return 3
        if len(counter.keys()) == 4:
            return 2
        return 1

    def __str__(self) -> str:
        return f"{self.cards} hand (bid {self.bid}) of type {self.type}"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other) -> bool:
        # 1st compare type
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False
        for s, o in zip(self.cards, other.cards):
            if card_values[s] < card_values[o]:
                return True
            if card_values[s] > card_values[o]:
                return False
        return True
    

card_values = {'2': 2,
               '3': 3,
               '4': 4,
               '5': 5,
               '6': 6,
               '7': 7,
               '8': 8,
               '9': 9,
               'T': 10,
               'J': 1,  #<- jokers
               'Q': 12,
               'K': 13,
               'A': 14,

}


main(sys.argv)