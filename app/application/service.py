from app.domain.models import GridMap, Point, RouteResult
from app.domain.ports import RouteObserver, RouteStrategy
from app.infrastructure.strategies import AStarStrategy, DijkstraStrategy

class RouteService:
    def __init__(self, observers: list[RouteObserver] | None = None):
        self._strategies: dict[str, RouteStrategy] = {
            "astar": AStarStrategy(),
            "dijkstra": DijkstraStrategy(),
        }
        self._observers = observers or []

    def calculate(self, grid: GridMap, start: Point, goal: Point, strategy: str) -> RouteResult:
        if not grid.contains(start) or not grid.contains(goal):
            raise ValueError("Origen o destino fuera del mapa")
        if not grid.passable(start) or not grid.passable(goal):
            raise ValueError("Origen o destino bloqueado")
        selected = self._strategies.get(strategy.lower())
        if selected is None:
            raise ValueError(f"Estrategia no soportada: {strategy}")
        result = selected.find_route(grid, start, goal)
        for observer in self._observers:
            observer.on_route_calculated(result)
        return result

class CalculateRouteCommand:
    def __init__(self, service: RouteService, grid: GridMap, start: Point, goal: Point, strategy: str):
        self.service = service
        self.grid = grid
        self.start = start
        self.goal = goal
        self.strategy = strategy

    def execute(self) -> RouteResult:
        return self.service.calculate(self.grid, self.start, self.goal, self.strategy)
