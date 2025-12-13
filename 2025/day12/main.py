# --- Christmas Tree Farm ---

from __future__ import annotations
import re
import sys
from functools import lru_cache
from typing import List, Tuple, Iterable

Coord = Tuple[int, int]

REGION_RE = re.compile(r"^\s*(\d+)\s*x\s*(\d+)\s*:\s*(.*)$")
SHAPE_HDR_RE = re.compile(r"^\s*(\d+)\s*:\s*$")


def normalize(coords: Iterable[Coord]) -> Tuple[Coord, ...]:
    pts = list(coords)
    minx = min(x for x, _ in pts)
    miny = min(y for _, y in pts)
    return tuple(sorted((x - minx, y - miny) for x, y in pts))


def gen_orientations(shape: List[Coord]) -> List[Tuple[Coord, ...]]:
    def rot90(p: Coord) -> Coord:
        x, y = p
        return (y, -x)

    def flipx(p: Coord) -> Coord:
        x, y = p
        return (-x, y)

    variants = set()
    for do_flip in (False, True):
        cur = [flipx(p) for p in shape] if do_flip else shape[:]
        r = cur
        for _ in range(4):
            variants.add(normalize(r))
            r = [rot90(p) for p in r]
    return list(variants)



def bit_index(x: int, y: int, W: int) -> int:
    return y * W + x


def placements_for_shape(oris, W, H):
    masks = []
    for coords in oris:
        maxx = max(x for x, _ in coords)
        maxy = max(y for _, y in coords)
        if maxx + 1 > W or maxy + 1 > H:
            continue
        for dx in range(W - maxx):
            for dy in range(H - maxy):
                m = 0
                for x, y in coords:
                    m |= 1 << bit_index(x + dx, y + dy, W)
                masks.append(m)
    return masks



def parse_input(text: str):
    lines = [l.rstrip() for l in text.splitlines()]

    i = 0
    shapes = []
    while i < len(lines):
        if REGION_RE.match(lines[i]):
            break
        if not lines[i]:
            i += 1
            continue

        m = SHAPE_HDR_RE.match(lines[i])
        idx = int(m.group(1))
        i += 1

        grid = []
        while i < len(lines) and lines[i] and not SHAPE_HDR_RE.match(lines[i]):
            grid.append(lines[i])
            i += 1

        coords = [(x, y)
                  for y, row in enumerate(grid)
                  for x, c in enumerate(row) if c == "#"]

        minx = min(x for x, _ in coords)
        miny = min(y for _, y in coords)
        coords = [(x - minx, y - miny) for x, y in coords]

        while len(shapes) <= idx:
            shapes.append(None)
        shapes[idx] = coords

    regions = []
    for line in lines[i:]:
        if not line:
            continue
        m = REGION_RE.match(line)
        W, H = int(m.group(1)), int(m.group(2))
        counts = list(map(int, m.group(3).split()))
        regions.append((W, H, counts))

    return shapes, regions



def can_fit_region(W, H, counts, shapes, oris):
    n = len(shapes)
    if len(counts) < n:
        counts = counts + [0] * (n - len(counts))

    area = W * H
    full_mask = (1 << area) - 1

    cell_counts = [len(s) for s in shapes] 

    needed = sum(counts[i] * cell_counts[i] for i in range(n))
    if needed > area:
        return False

    placements = [placements_for_shape(oris[i], W, H) for i in range(n)]

    covering = [[] for _ in range(n)]
    for i in range(n):
        cov = [[] for _ in range(area)]
        for m in placements[i]:
            mm = m
            while mm:
                b = mm & -mm
                c = b.bit_length() - 1
                cov[c].append(m)
                mm -= b
        covering[i] = cov

    @lru_cache(None)
    def dfs(occ, rem):
        if all(x == 0 for x in rem):
            return True

        free = (~occ) & full_mask
        if free == 0:
            return False

        c = (free & -free).bit_length() - 1

        for i in range(n):
            if rem[i] == 0:
                continue
            for m in covering[i][c]:
                if m & occ == 0:
                    r2 = list(rem)
                    r2[i] -= 1
                    if dfs(occ | m, tuple(r2)):
                        return True

        free_cells = free.bit_count()
        needed_cells = sum(rem[i] * cell_counts[i] for i in range(n))
        if free_cells > needed_cells:
            if dfs(occ | (1 << c), rem):
                return True

        return False

    return dfs(0, tuple(counts))



def solve(text: str):
    shapes, regions = parse_input(text)
    oris = [gen_orientations(s) for s in shapes]

    ok = 0
    for W, H, counts in regions:
        if can_fit_region(W, H, counts, shapes, oris):
            ok += 1
    return ok


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))