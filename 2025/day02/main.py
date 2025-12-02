# --- Gift Shop ---


def parse(text: str):
    ranges = []
    for part in text.strip().split(","):
        part = part.strip()
        if not part:
            continue
        start_str, end_str = part.split("-")
        start = int(start_str)
        end = int(end_str)
        ranges.append((start, end))
    return ranges


def is_invalid_exact_two(n: int) -> bool:
    s = str(n)
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]


def is_invalid_at_least_two(n: int) -> bool:
    s = str(n)
    L = len(s)

    for chunk_len in range(1, L // 2 + 1):
        if L % chunk_len != 0:
            continue
        repeats = L // chunk_len
        if repeats < 2:
            continue
        chunk = s[:chunk_len]
        if chunk * repeats == s:
            return True

    return False


def part1(ranges) -> int:
    total = 0
    for start, end in ranges:
        for n in range(start, end + 1):
            if is_invalid_exact_two(n):
                total += n
    return total


def part2(ranges) -> int:
    total = 0
    for start, end in ranges:
        for n in range(start, end + 1):
            if is_invalid_at_least_two(n):
                total += n
    return total


def main():
    with open("input.txt") as f:
        text = f.read()

    ranges = parse(text)

    answer1 = part1(ranges)
    answer2 = part2(ranges)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()