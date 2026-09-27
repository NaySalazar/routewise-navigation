from pydantic import BaseModel, Field

class PointSchema(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)

class RoutePayload(BaseModel):
    width: int = Field(default=40, ge=2, le=500)
    height: int = Field(default=40, ge=2, le=500)
    start: PointSchema
    goal: PointSchema
    blocked: list[PointSchema] = []
    strategy: str = "astar"

class RouteResponse(BaseModel):
    strategy: str
    cost: float
    visited_nodes: int
    elapsed_ms: float
    path_length: int
    path: list[list[int]]
