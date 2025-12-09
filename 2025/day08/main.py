# --- Playground ---


def parse(text):
    """
    Svaka linija: "x,y,z".
    """
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str, z_str = line.split(",")
        x = int(x_str)
        y = int(y_str)
        z = int(z_str)
        points.append((x, y, z))
    return points


def build_pairs(points):
    """
    Napravi listu svih parova (dist2, i, j), gdje je dist2 kvadrat distance
    između tačaka i i j.

    dist2 = (dx)^2 + (dy)^2 + (dz)^2
    """
    pairs = []
    n = len(points)
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist2 = dx * dx + dy * dy + dz * dz
            pairs.append((dist2, i, j))
    pairs.sort(key=lambda t: t[0])
    return pairs


class DisjointSet:
    """
    Disjoint Set struktura za spajanje komponenti.
    """

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        # path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        """
        Spoji skupove u kojima se nalaze a i b.
        Vraća True ako je stvarno došlo do spajanja (bile su različite komponente),
        False ako su već bile u istom skupu.
        """
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def multiply_three_largest_component_sizes(points, k_pairs: int) -> int:
    """
    Glavna logika:

    - points: lista tačaka (x, y, z)
    - k_pairs: koliko najbližih parova povezujemo (npr. 1000)

    Vraća proizvod veličina tri najveće komponente.
    """
    n = len(points)
    if n == 0:
        return 0

    pairs = build_pairs(points)
    dsu = DisjointSet(n)

    # Uzimamo prvih k_pairs parova (ili manje ako ih nema toliko)
    limit = min(k_pairs, len(pairs))
    for idx in range(limit):
        _, i, j = pairs[idx]
        # Povezujemo i, j (ako su već u istom skupu, union neće ništa promijeniti,
        # ali ovaj par se i dalje računa među k_pairs)
        dsu.union(i, j)

    # Izračunaj veličine svih komponenti
    comp_sizes = {}
    for i in range(n):
        r = dsu.find(i)
        comp_sizes.setdefault(r, 0)
        comp_sizes[r] += 1

    sizes = sorted(comp_sizes.values(), reverse=True)
    if len(sizes) < 3:
        # Ako ima manje od tri komponente, možemo ili:
        # - vratiti proizvod onih koje postoje, ili
        # - pretpostaviti da ulaz garantuje >= 3.
        from functools import reduce
        import operator
        return reduce(operator.mul, sizes, 1)

    return sizes[0] * sizes[1] * sizes[2]

def last_connection_x_product(points) -> int:
    """
    Part 2:

    - Sortiramo sve parove po distanci.
    - Spajamo nepovezane parove sve dok ne ostane jedna komponenta.
    - Vraćamo produkt X koordinata dva posljednja spojena boksa.
    """
    n = len(points)
    if n == 0:
        return 0

    pairs = build_pairs(points)
    dsu = DisjointSet(n)
    components = n
    last_edge = None

    for dist2, i, j in pairs:
        # spajamo samo ako nisu već u istom kolu
        if dsu.union(i, j):
            components -= 1
            last_edge = (i, j)
            if components == 1:
                break

    if last_edge is None:
        # već su bili svi povezani ili nema dovoljno tačaka
        return 0

    i, j = last_edge
    x1, _, _ = points[i]
    x2, _, _ = points[j]
    return x1 * x2



def part1(text: str) -> int:
    """
    Part 1:
    Poveži 1000 parova razvodnih kutija koje su međusobno najbliže
    i vrati proizvod veličina tri najveća kola.
    """
    points = parse(text)
    return multiply_three_largest_component_sizes(points, k_pairs=1000)


def part2(text: str) -> int:
    """
    Part 2:
    Nastavljamo spajati najbliže nepovezane parove dok svi boksovi
    ne budu u jednom kolu. Vraćamo produkt X koordinata
    posljednja dva spojena boksa.
    """
    points = parse(text)
    return last_connection_x_product(points)


def main():
    with open("input.txt") as f:
        text = f.read()

    answer1 = part1(text)
    answer2 = part2(text)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()
