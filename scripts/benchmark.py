import json
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.application.service import RouteService
from app.domain.models import GridMap

random.seed(42)
service = RouteService()

def build_map(size: int, obstacle_ratio: float = 0.18) -> GridMap:
    blocked = set()
    for x in range(size):
        for y in range(size):
            if (x, y) in {(0, 0), (size-1, size//4)}:
                continue
            if random.random() < obstacle_ratio:
                blocked.add((x, y))
    # Keep a guaranteed corridor on top/right edges.
    for x in range(size): blocked.discard((x, 0))
    for y in range(size): blocked.discard((size-1, y))
    return GridMap(size, size, blocked)

results = []
for size in (40, 80, 120):
    grid = build_map(size)
    for strategy in ("dijkstra", "astar"):
        samples = []
        visited = []
        costs = []
        for _ in range(30):
            result = service.calculate(grid, (0, 0), (size-1, size//4), strategy)
            samples.append(result.elapsed_ms)
            visited.append(result.visited_nodes)
            costs.append(result.cost)
        results.append({
            "size": f"{size}x{size}",
            "strategy": strategy,
            "mean_ms": round(statistics.mean(samples), 4),
            "p95_ms": round(statistics.quantiles(samples, n=20, method="inclusive")[18], 4),
            "visited_mean": round(statistics.mean(visited), 1),
            "cost": costs[-1]
        })

out = Path(__file__).resolve().parents[1] / "docs" / "benchmark_results.json"
out.write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
