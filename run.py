import heapq
import sys
from math import inf

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
DOORS = (2, 4, 6, 8)
STOPS = (0, 1, 3, 5, 7, 9, 10)
TARGET_ROOM= {'A': 0, 'B': 1, 'C': 2, 'D': 3}


def is_path_clear(hall: tuple, start: int, end: int) -> bool:
    if end < start:
        return not ('A' in hall[end:start]
                    or 'B' in hall[end:start]
                    or 'C' in hall[end:start]
                    or 'D' in hall[end:start])

    return not ('A' in hall[start + 1:end + 1]
                or 'B' in hall[start + 1: end + 1]
                or 'C' in hall[start + 1:end + 1]
                or 'D' in hall[start + 1:end + 1])


def parse(lines: list[str]):
    rooms = ()
    hall = tuple(lines[1][1:-1])
    room_a, room_b, room_c, room_d = [], [], [], []
    for line in lines[2:-1]:
        parts = list(filter(str.strip, line.split('#')))
        room_a.append(parts[0])
        room_b.append(parts[1])
        room_c.append(parts[2])
        room_d.append(parts[3])
    rooms += (tuple(room_a), tuple(room_b), tuple(room_c), tuple(room_d))

    return hall, rooms


def is_room_clean_for(t: str, room: tuple) -> bool:
    types = ['A', 'B', 'C', 'D']
    types.remove(t)
    for i in types:
        if i in room:
            return False

    return True


def get_top_type(room: tuple) -> tuple[int, str] | None:
    for i in range(len(room)):
        if room[i] != '.':
            return i, room[i]

    return None


def get_index_of_depth(room: tuple) -> int:
    d = len(room)
    for i in range(d):
        if room[i] != '.':
            return i - 1

    return d - 1


def is_placed(room: tuple, i: int, room_i: int, t: str) -> bool:
    if TARGET_ROOM[t] != room_i:
        return False
    for j in range(i + 1, len(room)):
        if room[j] != t:
            return False

    return True


def is_room_full_correct(room:tuple, room_i: int) -> bool:
    for j in room:
        if j == '.' or TARGET_ROOM[j] != room_i:
            return False

    return True


def move_from_hall(hall: tuple, rooms: tuple) -> list[tuple]:
    res = []
    for stop in STOPS:
        if hall[stop] == '.':
            continue
        t = hall[stop]
        room_i = TARGET_ROOM[t]
        if is_path_clear(hall, stop, DOORS[room_i]):
            if is_room_clean_for(t, rooms[room_i]):
                i = get_index_of_depth(rooms[room_i])
                if i == -1:
                    continue
                steps = abs(stop - DOORS[room_i]) + (i + 1)
                cost = steps * COSTS[t]
                new_hall = hall[:stop] + ('.', ) + hall[stop + 1:]
                new_room = rooms[room_i][:i] + (t, ) + rooms[room_i][i + 1:]
                new_rooms = rooms[:room_i] + (new_room, ) + rooms[room_i + 1:]
                res.append((new_hall, new_rooms, cost))

    return res


def move_from_room(hall: tuple, rooms: tuple) -> list[tuple]:
    res = []
    for i in range(len(rooms)):
        if is_room_full_correct(rooms[i], i):
            continue
        top = get_top_type(rooms[i])
        if not top:
            continue
        ind, t = top
        door = DOORS[i]
        stop_left = door - 1
        while stop_left >= 0 and hall[stop_left] == '.':
            if stop_left in STOPS:
                steps = (door - stop_left) + (ind + 1)
                cost = steps * COSTS[t]
                new_room = rooms[i][:ind] + ('.', ) + rooms[i][ind + 1:]
                new_rooms = rooms[:i] + (new_room,) + rooms[i + 1:]
                new_hall = hall[:stop_left] + (t, ) + hall[stop_left + 1:]
                res.append((new_hall, new_rooms, cost))
            stop_left -= 1

        stop_right = door + 1
        while stop_right <= 10 and hall[stop_right] == '.':
            if stop_right in STOPS:
                steps = (stop_right - door) + (ind + 1)
                cost = steps * COSTS[t]
                new_room = rooms[i][:ind] + ('.',) + rooms[i][ind + 1:]
                new_rooms = rooms[:i] + (new_room,) + rooms[i + 1:]
                new_hall = hall[:stop_right] + (t,) + hall[stop_right + 1:]
                res.append((new_hall, new_rooms, cost))
            stop_right += 1

    return res


def is_goal(hall: tuple, rooms: tuple) -> bool:
    for ch in hall:
        if ch != '.':
            return False

    for i in range(len(rooms)):
        for j in range(len(rooms[i])):
            if TARGET_ROOM[rooms[i][j]] != i:
                return False

    return True


def summary(hall: tuple, rooms: tuple) -> list[tuple]:
    l1 = move_from_hall(hall, rooms)
    l2 = move_from_room(hall, rooms)

    return l1 + l2


def get_heuristic(hall: tuple, rooms: tuple) -> int:
    s = 0
    for stop in STOPS:
        t = hall[stop]
        if t != '.':
            s += (abs(stop - DOORS[TARGET_ROOM[t]]) + 1) * COSTS[t]
    for j in range(len(rooms)):
        for k in range(len(rooms[j])):
            t = rooms[j][k]
            if t == '.':
                continue
            if j != TARGET_ROOM[t] or (not is_placed(rooms[j], k, j, t)):
                depth_up = k + 1
                s += (abs(DOORS[j] - DOORS[TARGET_ROOM[t]]) + 1 + depth_up) * COSTS[t]

    return s


def solve(lines: list[str]) -> int:
    hall, rooms = parse(lines)
    start = (hall, rooms)
    g_best = {start: 0}
    counter = 0
    h0 = get_heuristic(hall, rooms)
    heap = [(h0, counter, 0, hall, rooms)]

    while heap:
        f, _, g, hall, rooms = heapq.heappop(heap)

        if g != g_best.get((hall, rooms), None):
            continue

        if is_goal(hall, rooms):
            return g

        for new_hall, new_room, move_cost in summary(hall, rooms):
            new_g = g + move_cost
            key = (new_hall, new_room)
            if new_g < g_best.get(key, inf):
                g_best[key] = new_g
                counter += 1
                h = get_heuristic(new_hall, new_room)
                heapq.heappush(heap, (new_g + h, counter, new_g, new_hall, new_room))

    return 0


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()