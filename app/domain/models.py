from dataclasses import dataclass
from typing import Iterable

Point = tuple[int, int]

@dataclass(frozen=True)
class RouteRequest:
    start: Point
    goal: Point
    strategy: str = "astar"

@dataclass(frozen=True)
class RouteResult:
    path: list[Point]
    cost: float
    visited_nodes: int
    elapsed_ms: float
    strategy: str

class GridMap:
    def __init__(self, width: int, height: int, blocked: Iterable[Point] | None = None):
        if width < 2 or height < 2:
            raise ValueError("El mapa debe ser al menos de 2x2")
        self.width = width
        self.height = height
        self.blocked = set(blocked or [])

    def contains(self, point: Point) -> bool:
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, point: Point) -> bool:
        return point not in self.blocked

    def neighbors(self, point: Point) -> list[Point]:
        x, y = point
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [p for p in candidates if self.contains(p) and self.passable(p)]
