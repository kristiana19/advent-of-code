# --- Movie Theater ---

from collections import deque


def parse(text):
    """
    Ulazni tekst u listu crvenih pločica kao 2D koordinate (x, y).
    Svaka linija: 'x,y'.
    """
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str = line.split(",")
        x = int(x_str)
        y = int(y_str)
        points.append((x, y))
    return points


# ------------------ PART 1 ------------------


def area(a, b):
    ax, ay = a
    bx, by = b
    dx = abs(ax - bx) + 1
    dy = abs(ay - by) + 1
    return dx * dy


def part1(text: str) -> int:
    """
    Part 1:
    Najveća površina pravougaonika sa dva crvena polja kao suprotni uglovi.
    """
    points = parse(text)
    if len(points) < 2:
        return 0

    return max(area(a, b) for a in points for b in points)


# ------------------ PART 2 ------------------


def perimeter(points):
    """
    points: lista tačaka (x, y) u nekom koordinatnom sistemu (ovdje: kompresovane koordinate).

    Vraća skup svih tačaka na 'ivici' (perimetru) poligona definisanog tim tačkama,
    spajajući svaku tačku sa sljedećom (wrap zadnja -> prva) horizontalno ili vertikalno.
    """
    result = set()
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        ax, ay = points[i]
        bx, by = points[j]
        dx = bx - ax
        dy = by - ay
        sx = dx // abs(dx) if dx else 0
        sy = dy // abs(dy) if dy else 0
        if sx:  # horizontalni segment
            for x in range(ax, bx + sx, sx):
                result.add((x, ay))
        else:   # vertikalni segment
            for y in range(ay, by + sy, sy):
                result.add((ax, y))
    return result


def fill(points):
    """
    Flood fill 'spolja' da pronađemo koje ćelije su izvan poligona.

    points: skup tačaka koje čine perimetar (u nekom gridu).

    Vraća skup tačaka koje su izvan (outside).
    """
    x0 = min(x for x, y in points)
    x1 = max(x for x, y in points)
    y0 = min(y for x, y in points)
    y1 = max(y for x, y in points)

    # malo proširimo bounding box
    x0 -= 1
    x1 += 1
    y0 -= 1
    y1 += 1

    boundary = set(points)
    outside = set([(x0, y0)])
    Q = [(x0, y0)]

    while Q:
        x, y = Q.pop()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx and dy:
                    continue  # bez dijagonale
                nx = x + dx
                ny = y + dy
                if nx < x0 or ny < y0 or nx > x1 or ny > y1:
                    continue
                if (nx, ny) in outside:
                    continue
                if (nx, ny) in boundary:
                    continue
                outside.add((nx, ny))
                Q.append((nx, ny))

    return outside


def part2(text: str) -> int:
    """
    Part 2:
    Pravougaonik mora imati crvene pločice u suprotnim uglovima,
    a sve pločice unutar moraju biti crvene ili zelene.

    """
    points = parse(text)
    if len(points) < 2:
        return 0

    # 1) osnovne koordinate
    xs = sorted(set(x for x, y in points))
    ys = sorted(set(y for x, y in points))

    # ps, qs: "razvučene" koordinate (originalne + susjedi +/-1)
    ps = sorted(set(v for x in xs for v in (x - 1, x, x + 1)))
    qs = sorted(set(v for y in ys for v in (y - 1, y, y + 1)))

    # mape original -> indeks u ps/qs
    pl = {x: i for i, x in enumerate(ps)}
    ql = {y: i for i, y in enumerate(qs)}

    def compress(x, y):
        return (pl[x], ql[y])

    def dense(points_):
        """
        Kompresuje, računa perimetar i popunjava spolja.
        Vraća skup 'outside' tačaka u kompresovanom gridu.
        """
        pts = [compress(*p) for p in points_]
        per = perimeter(pts)
        out = fill(per)
        return out

    def valid(outside, a, b):
        """
        Provjera da li je pravougaonik (u kompresovanim koordinatama a..b)
        potpuno UNUTAR (dakle ne sadrži nijednu 'outside' tačku).
        """
        ax, ay = a
        bx, by = b
        x0, x1 = min(ax, bx), max(ax, bx)
        y0, y1 = min(ay, by), max(ay, by)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if (x, y) in outside:
                    return False
        return True

    outside = dense(points)
    compressed = [compress(*p) for p in points]

    def valid_area(a, b):
        """
        Ako je pravougaonik između a i b (kompresovane koordinate) validan,
        vraća njegovu površinu računatu u 'pravim' koordinatama (ps, qs).
        Inače 0.
        """
        if not valid(outside, a, b):
            return 0
        ax, ay = a
        bx, by = b
        ax, ay = ps[ax], qs[ay]
        bx, by = ps[bx], qs[by]
        dx = abs(ax - bx) + 1
        dy = abs(ay - by) + 1
        return dx * dy

    best = 0
    for a in compressed:
        for b in compressed:
            cur = valid_area(a, b)
            if cur > best:
                best = cur

    return best




def main():
    with open("input.txt") as f:
        text = f.read()

    answer1 = part1(text)
    answer2 = part2(text)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()
