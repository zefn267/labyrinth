import collections
import sys
from collections import defaultdict


def bfs(graph: dict[str, set], start) -> tuple[dict, dict]:
    queue = [start]
    dist = {start: 0}
    prev_v = {start: None}
    first_step = {}

    while queue:
        l = sorted(queue)
        queue.clear()

        for v in l:
            for u in sorted(graph.get(v)):
                n_dist = dist[v] + 1
                if u not in dist:
                    dist[u] = n_dist
                    prev_v[u] = v
                    if v == start:
                        first_step[u] = u
                    else:
                        first_step[u] = first_step[v]
                    queue.append(u)
                elif n_dist == dist[u]:
                    if v == start:
                        n_first = u
                    else:
                        n_first = first_step[v]
                    cur_first = first_step[u]
                    if n_first < cur_first or (n_first == cur_first and v < prev_v[u]):
                        prev_v[u] = v
                        first_step[u] = n_first

    return dist, prev_v


def get_gateway_and_prev(graph: dict[str, set], virus: str):
    dist, prev = bfs(graph, virus)
    gateways = [(k, v) for k, v in dist.items() if k.isupper()]
    if not gateways:
        return None
    gateway, _ = min(gateways, key=lambda x: (x[1], x[0]))

    return gateway, prev


def is_safe(graph: dict[str, set], virus: str, v: str, u: str) -> bool:
    graph[v].remove(u)
    graph[u].remove(v)

    edge = get_gateway_and_prev(graph, virus)
    if edge is None:
        return True
    gateway, prev = edge

    return prev[gateway] != virus


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for edge in edges:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])

    virus = 'a'
    result = []

    while True:
        if get_gateway_and_prev(graph, virus) is None:
            break

        candidates = []
        for v in graph.keys():
            if v.isupper():
                for u in graph[v]:
                    candidates.append((v, u))
        candidates.sort()

        for v, u in candidates:
            if is_safe(graph, virus, v, u):
                result.append(f'{v}-{u}')
                break
            graph[u].add(v)
            graph[v].add(u)

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
