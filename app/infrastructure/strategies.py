import heapq
import time
from typing import Optional

from app.domain.models import GridMap, Point, RouteResult
from app.domain.ports import RouteStrategy


def _reconstruct(came_from: dict[Point, Optional[Point]], goal: Point) -> list[Point]:
    path: list[Point] = []
    current: Optional[Point] = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


class DijkstraStrategy(RouteStrategy):
    name = "dijkstra"

    def find_route(self, grid: GridMap, start: Point, goal: Point) -> RouteResult:
        t0 = time.perf_counter()
        frontier: list[tuple[float, Point]] = [(0.0, start)]
        came_from: dict[Point, Optional[Point]] = {start: None}
        cost_so_far: dict[Point, float] = {start: 0.0}
        visited = 0

        while frontier:
            current_cost, current = heapq.heappop(frontier)
            if current_cost != cost_so_far.get(current):
                continue
            visited += 1
            if current == goal:
                break
            for nxt in grid.neighbors(current):
                new_cost = current_cost + 1.0
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    heapq.heappush(frontier, (new_cost, nxt))
                    came_from[nxt] = current

        if goal not in came_from:
            raise ValueError("No existe una ruta entre origen y destino")
        elapsed = (time.perf_counter() - t0) * 1000
        path = _reconstruct(came_from, goal)
        return RouteResult(path, cost_so_far[goal], visited, elapsed, self.name)


class AStarStrategy(RouteStrategy):
    name = "astar"

    @staticmethod
    def heuristic(a: Point, b: Point) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_route(self, grid: GridMap, start: Point, goal: Point) -> RouteResult:
        t0 = time.perf_counter()
        frontier: list[tuple[float, float, Point]] = [(0.0, 0.0, start)]
        came_from: dict[Point, Optional[Point]] = {start: None}
        g_score: dict[Point, float] = {start: 0.0}
        visited = 0

        while frontier:
            _, current_g, current = heapq.heappop(frontier)
            if current_g != g_score.get(current):
                continue
            visited += 1
            if current == goal:
                break
            for nxt in grid.neighbors(current):
                tentative = current_g + 1.0
                if nxt not in g_score or tentative < g_score[nxt]:
                    g_score[nxt] = tentative
                    f_score = tentative + self.heuristic(nxt, goal)
                    heapq.heappush(frontier, (f_score, tentative, nxt))
                    came_from[nxt] = current

        if goal not in came_from:
            raise ValueError("No existe una ruta entre origen y destino")
        elapsed = (time.perf_counter() - t0) * 1000
        path = _reconstruct(came_from, goal)
        return RouteResult(path, g_score[goal], visited, elapsed, self.name)
