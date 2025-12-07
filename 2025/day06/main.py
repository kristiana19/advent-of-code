# --- Trash Compactor ---

def parse(text: str):
    """
    Pretvori ulaz u mrežu (grid) i pronađi blokove kolona (zadatke).
    """
    # uklonimo potpuno prazne linije
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() != ""]
    if not lines:
        return [], []

    width = max(len(line) for line in lines)
    grid = [list(line.ljust(width)) for line in lines]

    rows = len(grid)
    cols = width

    # pronađi blokove kolona odvojene praznim kolonama
    blocks = []
    c = 0
    while c < cols:
        # preskoči prazne kolone
        while c < cols and all(grid[r][c] == " " for r in range(rows)):
            c += 1
        if c >= cols:
            break
        start = c
        # idi dokle god ima bar jedan neprazan znak u koloni
        while c < cols and any(grid[r][c] != " " for r in range(rows)):
            c += 1
        end = c - 1
        blocks.append((start, end))

    return grid, blocks


def solve_block_lr(grid, start_col, end_col):
    """
    PART 1:
    U jednom bloku (start_col..end_col), brojevi su po redovima (horizontalno),
    operator je u posljednjem redu.
    """
    rows = len(grid)

    # nađi operator u zadnjem redu
    op = None
    for c in range(start_col, end_col + 1):
        ch = grid[rows - 1][c]
        if ch in "+*":
            op = ch
            break
    if op is None:
        raise ValueError("Nije pronađen operator + ili * u bloku.")

    # čitamo brojeve po redovima iznad operatora
    numbers = []
    for r in range(rows - 1):
        segment = "".join(grid[r][c] for c in range(start_col, end_col + 1)).strip()
        if segment != "":
            numbers.append(int(segment))

    if not numbers:
        return 0

    if op == "+":
        return sum(numbers)
    else:
        produkt = 1
        for n in numbers:
            produkt *= n
        return produkt


def solve_block_rtl(grid, start_col, end_col):
    """
    PART 2:
    U jednom bloku, brojevi su po kolonama (vertikalno),
    čitaju se od desne ka lijevoj (right-to-left).
    Operator je i dalje u posljednjem redu.
    """
    rows = len(grid)

    # nađi operator u zadnjem redu (ista logika kao gore)
    op = None
    for c in range(start_col, end_col + 1):
        ch = grid[rows - 1][c]
        if ch in "+*":
            op = ch
            break
    if op is None:
        raise ValueError("Nije pronađen operator + ili * u bloku.")

    numbers = []
    # prolazimo kolone od desne ka lijevoj unutar bloka
    for c in range(end_col, start_col - 1, -1):
        # pokupimo cifre iz svih redova iznad operatora
        digits = [grid[r][c] for r in range(rows - 1) if grid[r][c].isdigit()]
        if digits:
            broj = int("".join(digits))
            numbers.append(broj)

    if not numbers:
        return 0

    if op == "+":
        return sum(numbers)
    else:
        produkt = 1
        for n in numbers:
            produkt *= n
        return produkt


def part1(text: str) -> int:
    grid, blocks = parse(text)
    total = 0
    for (start, end) in blocks:
        total += solve_block_lr(grid, start, end)
    return total


def part2(text: str) -> int:
    grid, blocks = parse(text)
    total = 0
    for (start, end) in blocks:
        total += solve_block_rtl(grid, start, end)
    return total


def main():
    with open("input.txt") as f:
        text = f.read()

    answer1 = part1(text)
    answer2 = part2(text)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()
