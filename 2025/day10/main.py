# --- Factory ---

import re
from collections import deque
from heapq import heappush, heappop
from typing import List, Tuple
import pulp


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


def fewest_presses_joltage(targets: List[int], buttons: List[int]) -> int:
    """
    A* pretraga po stanjima (c0..cn-1), monotono (+1).
    Cilj: tačno targets, min broj pritisaka.
    """
    n = len(targets)
    start = tuple([0] * n)
    goal = tuple(targets)

    if start == goal:
        return 0
    if not buttons:
        return float("inf")

    # precompute button -> list of indices
    btn_idxs: List[List[int]] = []
    btn_masks: List[int] = []
    for bm in buttons:
        if bm == 0:
            continue
        btn_masks.append(bm)
        idxs = []
        x = bm
        while x:
            b = x & -x
            idxs.append(b.bit_length() - 1)
            x -= b
        btn_idxs.append(idxs)

    if not btn_idxs:
        return float("inf")

    # quick impossibility: svaki counter koji treba > 0 mora biti pogođen bar jednim dugmetom
    affect = 0
    for bm in btn_masks:
        affect |= bm
    for i, t in enumerate(targets):
        if t > 0 and ((affect >> i) & 1) == 0:
            return float("inf")

    all_mask = (1 << n) - 1


    subsets = set()
    subsets.add(all_mask)
    for i in range(n):
        subsets.add(1 << i)
    for bm in btn_masks:
        subsets.add(bm)
        subsets.add(all_mask ^ bm)
    subsets = [m for m in subsets if m != 0]

    kS = {}
    for S in subsets:
        best = 0
        for bm in btn_masks:
            best = max(best, (bm & S).bit_count())
        kS[S] = best  # može biti 0

    def h(state: Tuple[int, ...]) -> int:
        rem = [targets[i] - state[i] for i in range(n)]
        lb = max(rem)  # bar toliko pressova jer svaki press diže counter max za 1

        for S in subsets:
            k = kS[S]
            if k == 0:
                continue
            s = 0
            mm = S
            while mm:
                b = mm & -mm
                i = b.bit_length() - 1
                s += rem[i]
                mm -= b
            lb = max(lb, (s + k - 1) // k)
        return lb

    pq = []
    heappush(pq, (h(start), 0, start))
    best_g = {start: 0}

    while pq:
        f, g, state = heappop(pq)
        if state == goal:
            return g
        if best_g.get(state) != g:
            continue

        # probaj sva dugmad
        for idxs in btn_idxs:
            ns = list(state)
            ok = True
            for i in idxs:
                if ns[i] >= targets[i]:  # ne smiješ preći target
                    ok = False
                    break
                ns[i] += 1
            if not ok:
                continue

            nxt = tuple(ns)
            ng = g + 1
            if ng < best_g.get(nxt, 10**18):
                best_g[nxt] = ng
                heappush(pq, (ng + h(nxt), ng, nxt))

    return float("inf")

def part2(text: str) -> int:
    """
    Part 2:
      min sum(x_j)
      s.t. za svaki counter i: sum_j A[i][j] * x_j == target[i]
      x_j >= 0, integer
    """
    total = 0

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # buttons iz parse_line
        _, buttons = parse_line(line)

        # targets iz {...}
        jm = re.search(r"\{([^}]*)\}", line)
        if not jm:
            raise ValueError(f"Nema joltage dijela {{...}} u liniji: {line}")
        targets = [int(x.strip()) for x in jm.group(1).split(",") if x.strip() != ""]

        # n iz [pattern]
        mpat = re.search(r"\[([.#]+)\]", line)
        if not mpat:
            raise ValueError(f"Nema [pattern] u liniji: {line}")
        n = len(mpat.group(1))

        if len(targets) != n:
            raise ValueError(f"Targets ({len(targets)}) != n ({n}) u liniji:\n{line}")

        # napravi matricu A[i][j] = 1 ako dugme j pogađa counter i
        A = [[0] * len(buttons) for _ in range(n)]
        for j, bm in enumerate(buttons):
            for i in range(n):
                if (bm >> i) & 1:
                    A[i][j] = 1

        # quick impossibility: counter sa target > 0 mora imati bar jedno dugme
        for i in range(n):
            if targets[i] > 0 and all(A[i][j] == 0 for j in range(len(buttons))):
                raise ValueError(f"Nemoguće: counter {i} ima target {targets[i]} a nema dugmeta. Linija:\n{line}")

        # ILP
        prob = pulp.LpProblem("joltage", pulp.LpMinimize)

        xs = [pulp.LpVariable(f"x{j}", lowBound=0, cat="Integer") for j in range(len(buttons))]

        # objective: minimize total presses
        prob += pulp.lpSum(xs)

        # constraints: exact targets
        see = []
        for i in range(n):
            prob += pulp.lpSum(A[i][j] * xs[j] for j in range(len(buttons))) == targets[i]

        # solve (CBC)
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[status] != "Optimal":
            raise ValueError(f"Nije našao optimalno rješenje (status={pulp.LpStatus[status]}). Linija:\n{line}")

        presses = int(pulp.value(prob.objective))
        total += presses

    return total



def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    answer1 = part1(text)
    answer2 = part2(text)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()