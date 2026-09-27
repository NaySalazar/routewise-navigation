from fastapi.testclient import TestClient
from app.main import app
from app.application.service import RouteService
from app.domain.models import GridMap

client = TestClient(app)

def test_health():
    assert client.get('/health').json() == {"status": "ok"}

def test_astar_and_dijkstra_have_same_optimal_cost():
    grid = GridMap(20, 20, blocked={(5, y) for y in range(19)})
    service = RouteService()
    a = service.calculate(grid, (0, 0), (19, 19), "astar")
    d = service.calculate(grid, (0, 0), (19, 19), "dijkstra")
    assert a.cost == d.cost
    assert a.path[0] == (0, 0) and a.path[-1] == (19, 19)


def test_api_rejects_blocked_start():
    response = client.post('/routes', json={
        "width": 10,
        "height": 10,
        "start": {"x": 0, "y": 0},
        "goal": {"x": 9, "y": 9},
        "blocked": [{"x": 0, "y": 0}],
        "strategy": "astar"
    })
    assert response.status_code == 400
