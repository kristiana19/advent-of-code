# --- Laboratories ---


def parse(text: str):

    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() != ""]
    return lines


def simulate_beams(lines):
    """
    Ideja:

    - current[c] = koliko zraka/timeline-ova je trenutno u koloni c u ovom redu
    - za svaki red, za svaku kolonu:
        * ako ima zraka/timeline-ova (count > 0) na tom mjestu:
            - ako je '^' -> split:
                +1 split (Part 1)
                count timeline-ova ide lijevo-dole i count desno-dole
            - inače:
                count timeline-ova ide pravo dole

    Vraća:
      - splits: ukupan broj split događaja (Part 1)
      - timelines: ukupan broj timeline-ova na kraju (Part 2)
    """
    if not lines:
        return 0, 0

    width = len(lines[0])

    # 'S' je u prvom redu
    start_col = lines[0].index("S")

    current = [0] * width
    next_row = [0] * width

    # jedan "početni" zrak / čestica u koloni start_col
    current[start_col] = 1

    splits = 0

    # prolazimo red po red
    for row in lines:
        for i, count in enumerate(current):
            if count > 0:
                ch = row[i]
                if ch == "^":
                    # barem jedan zrak/timeline je stigao do splittera
                    splits += 1

                    # svi ti timeline-ovi se razdvajaju na lijevo i desno
                    if i > 0:
                        next_row[i - 1] += count
                    if i < width - 1:
                        next_row[i + 1] += count
                else:
                    # nema splittera, sve ide pravo dole
                    next_row[i] += count

        # prelazimo na sljedeći red
        current, next_row = next_row, current

        # resetujemo next_row na nule
        for j in range(width):
            next_row[j] = 0

    timelines = sum(current)
    return splits, timelines


def part1(text: str) -> int:
    """
    Part 1:
    Koliko puta je zrak bio razdijeljen (split) na splitterima '^'.
    """
    lines = parse(text)
    splits, _ = simulate_beams(lines)
    return splits


def part2(text: str) -> int:
    """
    Part 2:
    Koliko različitih timeline-ova nastane nakon što jedna čestica
    prođe kroz sve moguće putanje.
    """
    lines = parse(text)
    _, timelines = simulate_beams(lines)
    return timelines


def main():
    with open("input.txt") as f:
        text = f.read()

    answer1 = part1(text)
    answer2 = part2(text)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()
