# --- Lobby ---

def parse(text):         
    return text.strip().splitlines()   # "987654321111111"


def najveci_broj_iz_para(linija):
    najveci  = 0
    cifre = list(linija)

    for i in range(len(cifre)):
        for j in range(i + 1, len(cifre)):
            prva = int(cifre[i])
            druga = int(cifre[j])
            vrijednost = prva * 10 + druga

            if vrijednost > najveci:
                najveci = vrijednost

    return najveci


def najveca_12(linija):
    """
    Pronađi najveći mogući broj od tačno 12 cifara
    koji možeš dobiti iz ove linije, čuvajući redosled cifara.

    """
    cifre = list (linija.strip())
    m = 12
    n = len(cifre)

    # u slucaju da je cijeli string 12
    if n == m:
        return int(linija.strip())
    
    # koliko cifara smijemo izbaciti?
    ukloni = n - m
    stek = []

    for c in cifre:
        # [2]
        # [2, 3]
        # [2, 3, 4] ...
        # i zadnja cifra u steku je manja od nove cifre -> izbaci je
        while stek and ukloni > 0 and stek[-1] < c:
            stek.pop()
            ukloni -= 1
        
        stek.append(c)

        # NPR:

        # zadnja cifra 2 < 7 → izbaci
        # stek = [2,3,4]

        # zadnja cifra 4 < 7 → izbaci
        # stek = [2,3]

        # zadnja cifra 3 < 7 → izbaci
        # stek = [2]

        # zadnja cifra 2 < 7 → izbaci
        # stek = []

        # stek je prazan — petlja se prekida
        # dodaj 7 → stek = [7]
        

    if len(stek) > m: # ako i dalje imamo vise od 12, odrezi visak
            stek = stek[:m]

    return int("".join(stek))


def part1(linije):
    zbir = 0
    for linija in linije:
        zbir += najveci_broj_iz_para(linija)
    return zbir


def part2(linije):
    zbir = 0
    for linija in linije:
        zbir += najveca_12(linija)
    return zbir


def main():
    with open("input.txt") as f:
        text = f.read()

    linije = parse(text)

    answer1 = part1(linije)
    answer2 = part2(linije)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()