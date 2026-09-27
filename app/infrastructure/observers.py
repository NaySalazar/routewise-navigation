from dataclasses import asdict
from app.domain.models import RouteResult
from app.domain.ports import RouteObserver

class MetricsObserver(RouteObserver):
    def __init__(self) -> None:
        self.events: list[dict] = []

    def on_route_calculated(self, result: RouteResult) -> None:
        event = asdict(result)
        event["path_length"] = len(result.path)
        self.events.append(event)
