# --- Secret Entrance ---

def parse(input_text: str) -> list[int]:
    """Pretvori linije 'L68', 'R10', ... u listu pomaka (int)."""
    
    moves = [] #ovde cemo sakupljati sve pomake

    # strip() skine sve praznine na pocetku ili kraju
    # splitlines() razbije sve na redove
    for line in input_text.strip().splitlines():
        line = line.strip()

        if not line:
            # u slucaju da je linija prazna (""), preskacemo
            continue

        direction = line[0] # prvo slovo: 'L' ili 'R'
        amount_str = line[1:] # ostatak npr. "68"
        amount = int(amount_str) # ostatak pretvori u broj

        # ako je R onda je pozitivan pomak, ako je L onda je negativan
        if (direction == 'R') :
            delta = amount
        else :
            delta = -amount

        moves.append(delta)        

    return moves


def part1(moves: list[int]) -> int:
    dial = 50
    password = 0

    for delta in moves:
        dial += delta #pomjeri poziciju
        if dial % 100 == 0: #0.....99
            password += 1

    return password

def part2(moves: list[int]) -> int:
    dial = 50
    password = 0

    for delta in moves:
        if delta >= 0:
            # koliko puta predjemo neki visekratnik od 100 kad idemo u + smijeru
            password += (dial + delta) // 100
        else:
            # isto, ali kad idemo u negativnom smijeru
            password += (100 - dial - delta) // 100 - (100 - dial) // 100

        # normaliziramo dial na 0..99
        dial = (dial + delta) % 100

    return password


def main():
    with open("input.txt") as f:
        text = f.read()

    moves = parse(text)

    answer1 = part1(moves)
    answer2 = part2(moves)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()
