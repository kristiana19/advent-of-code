# --- Reactor ---


def parse(text: str):
    """
    Parsira ulaz u usmjereni graf.
    Svaka linija je oblika:
        ime: susjed1 susjed2 susjed3 ...
    """
    graph = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        left, right = line.split(":")
        node = left.strip()
        if right.strip() == "":
            neighbors = []
        else:
            neighbors = right.split()
        graph[node] = neighbors
    return graph


def count_paths(graph, start: str, target: str) -> int:
    """
    Vraća broj različitih putanja od start do target
    koristeći DFS + memoizaciju.
    """
    memo = {}
    visiting = set()

    def dfs(node: str) -> int:
        if node == target:
            return 1
        if node in memo:
            return memo[node]
        if node in visiting:
            return 0

        visiting.add(node)
        total = 0
        for nb in graph.get(node, []):
            total += dfs(nb)
        visiting.remove(node)

        memo[node] = total
        return total

    return dfs(start)

def count_paths_with_required(graph, start: str, target: str, required_nodes: list[str]) -> int:
    """
    Broj putanja od start do target koje MORAJU proći kroz sve čvorove u required_nodes
    (u bilo kom redoslijedu).

    Implementacija:
      - svako required čvoru dodijelimo bit u maski
      - stanje je (node, mask) gdje mask kaže koje required smo već posjetili
      - na cilju brojimo samo putanje gdje su svi bitovi uključeni
    """
    # mapiranje required node -> bit index
    req_index = {name: i for i, name in enumerate(required_nodes)}
    full_mask = (1 << len(required_nodes)) - 1

    memo = {}
    visiting = set()

    def dfs(node: str, mask: int) -> int:
        key = (node, mask)
        if key in memo:
            return memo[key]
        if key in visiting:
            # zaštita od potencijalnih ciklusa
            return 0

        # ažuriraj masku ako je trenutni node jedan od required
        if node in req_index:
            mask |= (1 << req_index[node])

        if node == target:
            # važi samo ako smo posjetili sve required
            return 1 if mask == full_mask else 0

        visiting.add(key)
        total = 0
        for nb in graph.get(node, []):
            total += dfs(nb, mask)
        visiting.remove(key)

        memo[key] = total
        return total

    return dfs(start, 0)


def part1(text: str) -> int:
    """
    Part 1:
    Koliko različitih putanja vodi od 'you' do 'out'?
    """
    graph = parse(text)
    return count_paths(graph, "you", "out")


def part2(text: str) -> int:
    """
    Part 2:
    Koliko putanja vodi od 'svr' do 'out' koje usput posjete i 'dac' i 'fft'?
    """
    graph = parse(text)
    return count_paths_with_required(graph, "svr", "out", ["dac", "fft"])


def main():
    with open("input.txt") as f:
        text = f.read()

    answer1 = part1(text)
    answer2 = part2(text)

    print("Part 1:", answer1)
    print("Part 2:", answer2)


if __name__ == "__main__":
    main()