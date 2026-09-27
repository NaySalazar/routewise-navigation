from abc import ABC, abstractmethod
from .models import GridMap, Point, RouteResult

class RouteStrategy(ABC):
    name: str

    @abstractmethod
    def find_route(self, grid: GridMap, start: Point, goal: Point) -> RouteResult:
        raise NotImplementedError

class RouteObserver(ABC):
    @abstractmethod
    def on_route_calculated(self, result: RouteResult) -> None:
        raise NotImplementedError
