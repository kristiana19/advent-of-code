# --- Factory ---

import re
from collections import deque


def parse_line(line: str):
    """
    Parsira jednu liniju:
    [.##.] (3) (1,3) (2) ... {ignoriši}

    Vraća:
      - target_mask (int)
      - listu button_mask-ova (list[int])
    """
    line = line.strip()
    if not line:
        return None, None

    # 1) uzmi šablon lampica u uglastim zagradama
    m = re.search(r"\[([.#]+)\]", line)
    if not m:
        raise ValueError(f"Nije pronađen šablon lampica u liniji: {line}")
    pattern = m.group(1)
    n = len(pattern)

    target_mask = 0
    for i, ch in enumerate(pattern):
        if ch == "#":
            target_mask |= (1 << i)

    # 2) nađi sva dugmad u zagradama ()
    #    (sve prije prve '{',  ignorisemo)
    before_brace = line.split("{", 1)[0]
    button_specs = re.findall(r"\(([^)]*)\)", before_brace)

    buttons = []
    for spec in button_specs:
        spec = spec.strip()
        if not spec:
            continue
        indices = [s.strip() for s in spec.split(",") if s.strip() != ""]
        mask = 0
        for idx_str in indices:
            idx = int(idx_str)
            if idx < 0 or idx >= n:
                raise ValueError(f"Indeks lampice {idx} je van opsega za šablon dužine {n}")
            mask |= (1 << idx)
        buttons.append(mask)

    return target_mask, buttons


def fewest_presses_for_machine(target_mask: int, buttons: list[int]) -> int:
    """
    BFS po stanjima (bitmaskama) da nađemo minimalan broj pritisaka
    da od 0 (sve ugašeno) dođemo do target_mask.
    """
    if target_mask == 0:
        return 0  # već smo u cilju

    if not buttons:
        # nema dugmadi, a cilj nije 0 -> nemoguće
        return float("inf")

    # broj lampica je maksimalan indeks bita u target_mask-u ili dugmadima
    max_bit = 0
    tmp = target_mask
    while tmp:
        max_bit = max(max_bit, tmp.bit_length())
        tmp &= tmp - 1
    for b in buttons:
        if b:
            max_bit = max(max_bit, b.bit_length())

    num_states = 1 << max_bit  # gornja granica stanja

    dist = [-1] * num_states
    start = 0
    dist[start] = 0

    q = deque([start])

    while q:
        state = q.popleft()
        d = dist[state]

        for bm in buttons:
            nxt = state ^ bm
            if nxt == target_mask:
                return d + 1
            if dist[nxt] == -1:
                dist[nxt] = d + 1
                q.append(nxt)

    return float("inf")  # teorijski, ako nije dostupan cilj


def part1(text: str) -> int:
    """
    Part 1:
    Za svaku mašinu (liniju), nađi minimalan broj pritisaka da se dobije
    zadani šablon lampica, pa sve saberi.
    """
    total_presses = 0

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        target_mask, buttons = parse_line(line)
        presses = fewest_presses_for_machine(target_mask, buttons)
        if presses == float("inf"):
            # ako je nemoguće, stavi error ili ignorisi
            # po zadatku se pretpostavlja da je uvijek moguće
            raise ValueError(f"Nije moguće konfigurirati mašinu za liniju: {line}")

        total_presses += presses

    return total_presses


def part2(text: str) -> int:
    return 0


def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    answer1 = part1(text)
    answer2 = part2(text)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()