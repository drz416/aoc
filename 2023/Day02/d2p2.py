
from pathlib import Path

def main():
    # Prep Code
    use_test_data = False
    data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
Game 15: 14 red"""
    lines: list[str] = data.splitlines()
    
    if use_test_data == False:
        data_file = Path.cwd() / "data.txt"
        with open(data_file, "r") as f:
            lines: list[str] = f.readlines()

    # Puzzle code
    limit_red = 12
    limit_green = 13
    limit_blue = 14
    sum = 0

    for row in lines:
        red = 0
        green = 0
        blue = 0
        
        row = row.strip()
        game_split = row.split(sep=": ")
        game = int(game_split[0][5:])
        sets = game_split[1]
        sets_split = sets.split(sep="; ")
        for st in sets_split:
            st_split = st.split(sep=", ")
            for dice in st_split:
                num = int(dice.split()[0])
                colour = dice.split()[1]
                if colour == "red":
                    red = max(red, num)
                elif colour == "green":
                    green = max(green, num)
                elif colour == "blue":
                    blue = max(blue, num)
                else:
                    print(f"Could not parse {row}")
                    raise TypeError
        power = red * green * blue
        sum += power
        print(f"{game}: red {red}, green {green}, blue {blue}, sum: {sum}")

main()
