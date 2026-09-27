# RouteWise Navigation

Prototipo académico para la actividad **Navegando mareas: Estrategias de navegación en la arquitectura de software**, Unidad 3 del curso Arquitectura de Software.

RouteWise expone una API REST capaz de calcular rutas óptimas sobre mapas en cuadrícula con obstáculos. La solución permite alternar entre **Dijkstra** y **A*** mediante el patrón **Strategy**, encapsula la solicitud con **Command** y registra métricas mediante **Observer**.

## Objetivo académico

Evaluar una arquitectura de navegación, identificar oportunidades de mejora y comprobar con métricas el efecto de una estrategia optimizada sobre rendimiento, escalabilidad y mantenibilidad.

## Arquitectura por capas

El proyecto sigue un diseño por capas para separar responsabilidades y facilitar la evolución del sistema:

- Capa de presentación: API REST con FastAPI.
- Capa de aplicación: comandos y servicios de caso de uso.
- Capa de dominio: modelos, rutas, validaciones y contratos de estrategia/observación.
- Capa de infraestructura: implementaciones de A*, Dijkstra y métricas del Observer.

## Arquitectura

```text
Usuario
  |
  v
RouteWise API
  |
  v
CalculateRouteCommand <<Command>>
  |
  v
RouteService
  |---------------------------|
  v                           v
RouteStrategy <<Strategy>>   MetricsObserver <<Observer>>
  |        |
  v        v
A*       Dijkstra
  \        /
    GridMap
```

## Patrones aplicados

| Patrón | Implementación | Propósito |
|---|---|---|
| Strategy | `AStarStrategy`, `DijkstraStrategy` | Cambiar el algoritmo de navegación sin modificar el servicio de aplicación. |
| Command | `CalculateRouteCommand` | Encapsular la solicitud de cálculo y desacoplar el endpoint del caso de uso. |
| Observer | `MetricsObserver` | Registrar métricas sin acoplar la lógica de cálculo a observabilidad. |

## Tecnologías

- Python 3.9+
- FastAPI
- Pydantic
- Pytest
- Docker / Docker Compose
- PlantUML (fuentes editables de diagramas)

## Estructura

```text
app/
  api/             Esquemas HTTP
  application/     Caso de uso y Command
  domain/          Modelo y puertos
  infrastructure/  Algoritmos Strategy y Observer

tests/             Pruebas automatizadas
scripts/           Benchmark reproducible
diagrams/          UML en PlantUML
docs/              Resultados de benchmark
```

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger/OpenAPI: `http://localhost:8000/docs`

## Ejecución con Docker

```bash
docker compose up --build
```

## API

### `GET /health`
Comprueba disponibilidad del servicio.

### `POST /routes`
Ejemplo:

```json
{
  "width": 30,
  "height": 30,
  "start": {"x": 1, "y": 1},
  "goal": {"x": 28, "y": 25},
  "blocked": [{"x": 10, "y": 4}, {"x": 10, "y": 5}],
  "strategy": "astar"
}
```

La respuesta incluye ruta, costo, tiempo de cálculo y número de nodos visitados.

### `GET /metrics`
Retorna las últimas métricas capturadas por el Observer.

Los endpoints reales del proyecto son:

- `GET /health`
- `POST /routes`
- `GET /metrics`

## Pruebas

```bash
pytest
```

Estado verificado durante la preparación de la entrega: **3 pruebas aprobadas**.

## Benchmark

```bash
python3 scripts/benchmark.py
```

Prueba sintética reproducible con semilla fija, 18 % de obstáculos y 30 ejecuciones por combinación.

| Mapa | Dijkstra media | A* media | Reducción de tiempo | Nodos Dijkstra | Nodos A* |
|---|---:|---:|---:|---:|---:|
| 40x40 | 2.5114 ms | 1.0218 ms | 59.30 % | 956 | 346 |
| 80x80 | 10.3604 ms | 3.8853 ms | 62.52 % | 3774 | 1293 |
| 120x120 | 23.5545 ms | 8.5845 ms | 63.58 % | 8513 | 2798 |

Los resultados son **métricas de laboratorio**, no un SLA de producción. En los tres tamaños A* conserva el mismo costo óptimo que Dijkstra y reduce de forma marcada el espacio explorado.

## UML

La carpeta `diagrams/` contiene fuentes PlantUML editables para:

- componentes;
- secuencia;
- clases;
- actividad.

## Escalabilidad y mantenibilidad

La lógica algorítmica está detrás del puerto `RouteStrategy`, lo que permite incorporar otras estrategias sin modificar el controlador ni el servicio principal. El prototipo es stateless por solicitud, por lo que el servicio HTTP puede replicarse horizontalmente detrás de un balanceador en una evolución cloud.

## Limitaciones

- El mapa reside en memoria y utiliza una cuadrícula simplificada.
- No incluye tráfico dinámico ni pesos por segmento.
- Las métricas del Observer son volátiles en memoria.
- El benchmark mide CPU local y no latencia de red ni infraestructura cloud.

## Propuesta de mejora ágil

Para una evolución ágil del proyecto, el siguiente backlog priorizado permite mejorar el valor académico y productivo sin romper la arquitectura actual:

1. Mejorar la observabilidad con historial persistente y panel básico de métricas.
2. Añadir validación de entrada y mapa de bloqueo más explícita en la API.
3. Gestionar caché de rutas frecuentes para reducir coste computacional en consultas repetidas.
4. Extender el dominio para soportar pesos por segmento y restricciones reales del mapa.
5. Preparar una segunda iteración con despliegue contenedorizado y pipeline de pruebas automatizadas.

## Mejoras futuras

- cachear rutas frecuentes mediante Cache-Aside;
- incorporar pesos dinámicos por tráfico;
- persistir grafos geoespaciales;
- distribuir métricas en un backend de observabilidad;
- añadir rate limiting y balanceo horizontal;
- evaluar variantes bidireccionales o jerárquicas para grafos mayores.

## Contexto académico

Este proyecto se presenta como entrega académica para la unidad de arquitectura de software y la actividad de navegación en entornos con múltiples estrategias de resolución. La solución enfatiza la comprensión de patrones estructurales y su validación empírica con pruebas y benchmark reproducibles.


- **Curso:** Arquitectura de Software
- **Unidad:** 3 - Evaluación y optimización de arquitecturas
- **Actividad:** Navegando mareas: Estrategias de navegación en la arquitectura de software
