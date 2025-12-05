# --- Cafeteria ---

def parse(text):
    """
    Vrati:
    - listu opsega (start, end)
    - listu dostupnih ID-jeva
    """
    lines = [line.strip() for line in text.strip().splitlines()]

    ranges = []
    ids = []

    in_ids_part = False

    for line in lines:
        if line == "":
            # prazan red -> odavde nadalje tretiramo kao ID-jeve
            in_ids_part = True
            continue

        if "-" in line and not in_ids_part:
            # linija opsega, npr "3-5"
            a, b = line.split("-")
            ranges.append((int(a), int(b)))
        else:
            # sve ostalo -> dostupni ID-jevi
            ids.append(int(line))

    return ranges, ids



def je_svjez(id_broj, opsezi):
    """
    Provjeri da li ID ulazi u bilo koji opseg.
    """
    for (a, b) in opsezi:
        if a <= id_broj <= b:
            return True
    return False


def part1(opsezi, dostupni):

    broj_svjezih = 0
    for x in dostupni:
        if je_svjez(x, opsezi):
            broj_svjezih += 1
    return broj_svjezih


def part2(opsezi):

    if not opsezi:
        return 0

    # 1. sortiramo opsege po početku
    opsezi_sortirani = sorted(opsezi, key=lambda x: x[0])

    spojeni = []
    trenutni_start, trenutni_end = opsezi_sortirani[0]

    for a, b in opsezi_sortirani[1:]:
        # ako se novi opseg preklapa ili dodiruje sa trenutnim
        if a <= trenutni_end + 1:
            # proširimo trenutni opseg
            if b > trenutni_end:
                trenutni_end = b
        else:
            # završavamo trenutni opseg i krećemo novi
            spojeni.append((trenutni_start, trenutni_end))
            trenutni_start, trenutni_end = a, b

    # ne zaboravi poslednji opseg
    spojeni.append((trenutni_start, trenutni_end))

    # 2. saberi dužine svih spojenih opsega
    ukupno = 0
    for a, b in spojeni:
        ukupno += (b - a + 1)

    return ukupno



def main():
    with open("input.txt") as f:
        text = f.read()

    opsezi, dostupni = parse(text)

    odgovor1 = part1(opsezi, dostupni)
    odgovor2 = part2(opsezi)

    print("Part 1:", odgovor1)
    print("Part 2:", odgovor2)


if __name__ == "__main__":
    main()
