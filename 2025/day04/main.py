# --- Printing Department ---

def parse(text):
    """
    Pretvori ulazni string u listu linija (mrežu).
    Svaka linija je string, npr. '..@@.@@@@.'
    """
    return text.strip().splitlines()


def broj_susednih_rolni(mreza, red, kolona):
    """
    Prebroj koliko ima '@' u osam susednih polja oko (red, kolona).
    mreza može biti lista stringova ili lista lista karaktera.
    """
    visina = len(mreza)
    sirina = len(mreza[0])
    broj = 0

    for dr in (-1, 0, 1):
        for dk in (-1, 0, 1):
            if dr == 0 and dk == 0:
                continue  # preskačemo samo centar

            nr = red + dr
            nk = kolona + dk

            if 0 <= nr < visina and 0 <= nk < sirina:
                if mreza[nr][nk] == '@':
                    broj += 1

    return broj


def part1(mreza):
    """
    Part 1:
    Vrati koliko rolni papira '@' su pristupačne viljuškaru
    u početnom stanju (manje od 4 susjedne rolne '@').
    """
    visina = len(mreza)
    sirina = len(mreza[0])
    pristupacne = 0

    for r in range(visina):
        for k in range(sirina):
            if mreza[r][k] == '@':
                susedi = broj_susednih_rolni(mreza, r, k)
                if susedi < 4:
                    pristupacne += 1

    return pristupacne


def part2(mreza):
    """
    Part 2:
    Simuliraj proces uklanjanja rolni:
    - pronađi sve pristupačne rolne ('@' sa < 4 susedne '@')
    - ukloni ih (pretvori u '.')
    - ponavljaj dok više nema pristupačnih rolni
    Vrati ukupan broj uklonjenih rolni.
    """
    # napravimo kopiju mreže (lista lista karaktera)
    grid = [list(red) for red in mreza]
    visina = len(grid)
    sirina = len(grid[0])
    ukupno_uklonjenih = 0

    while True:
        za_ukloniti = []

        # pronađi sve rolne koje su trenutno pristupačne
        for r in range(visina):
            for k in range(sirina):
                if grid[r][k] == '@':
                    susedi = broj_susednih_rolni(grid, r, k)
                    if susedi < 4:
                        za_ukloniti.append((r, k))

        # ako nema više ništa za uklanjanje, prekidamo
        if not za_ukloniti:
            break

        # ukloni sve označene rolne u ovom krugu
        for (r, k) in za_ukloniti:
            grid[r][k] = '.'

        ukupno_uklonjenih += len(za_ukloniti)

    return ukupno_uklonjenih


def main():
    with open("input.txt") as f:
        text = f.read()

    mreza = parse(text)

    odgovor1 = part1(mreza)
    odgovor2 = part2(mreza)

    print("Part 1:", odgovor1)
    print("Part 2:", odgovor2)


if __name__ == "__main__":
    main()