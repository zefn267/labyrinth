import collections
import sys
from collections import defaultdict


def bfs(graph: dict[str, set], start) -> tuple[dict, dict]:
    queue = collections.deque([start])
    dist = {start: 0}
    prev_v = {start: None}

    while queue:
        size = len(queue)
        nodes = [queue.popleft() for _ in range(size)]
        nodes.sort()
        for v in nodes:
            for u in sorted(graph.get(v, [])):
                if u not in dist:
                    dist[u] = dist[v] + 1
                    prev_v[u] = v
                    queue.append(u)

    return dist, prev_v


def get_gateway_and_prev(graph: dict[str, set], virus: str):
    dist, prev = bfs(graph, virus)
    gateways = [(k, v) for k, v in dist.items() if k.isupper()]
    if not gateways:
        return None
    gateway, _ = min(gateways, key=lambda x: (x[1], x[0]))

    return gateway, prev


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for edge in edges:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])

    virus = 'a'
    result = []

    while True:
        edge = get_gateway_and_prev(graph, virus)
        if edge is None:
            break
        gateway, prev = edge
        p = prev[gateway]
        result.append(f'{gateway}-{p}')
        graph[gateway].remove(p)
        graph[p].remove(gateway)

        edge = get_gateway_and_prev(graph, virus)
        if edge is None:
            break
        gateway, prev = edge
        x = gateway
        while prev[x] != virus:
            x = prev[x]
        virus = x

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()