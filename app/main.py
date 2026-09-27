from fastapi import FastAPI, HTTPException
from app.api.schemas import RoutePayload, RouteResponse
from app.application.service import CalculateRouteCommand, RouteService
from app.domain.models import GridMap
from app.infrastructure.observers import MetricsObserver

app = FastAPI(title="RouteWise Navigation API", version="1.0.0")
metrics = MetricsObserver()
service = RouteService([metrics])

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/routes", response_model=RouteResponse)
def calculate_route(payload: RoutePayload) -> RouteResponse:
    blocked = {(p.x, p.y) for p in payload.blocked}
    grid = GridMap(payload.width, payload.height, blocked)
    command = CalculateRouteCommand(
        service,
        grid,
        (payload.start.x, payload.start.y),
        (payload.goal.x, payload.goal.y),
        payload.strategy,
    )
    try:
        result = command.execute()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return RouteResponse(
        strategy=result.strategy,
        cost=result.cost,
        visited_nodes=result.visited_nodes,
        elapsed_ms=round(result.elapsed_ms, 4),
        path_length=len(result.path),
        path=[[x, y] for x, y in result.path],
    )

@app.get("/metrics")
def route_metrics() -> dict:
    return {"count": len(metrics.events), "events": metrics.events[-20:]}
