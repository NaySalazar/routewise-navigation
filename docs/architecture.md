# Decisiones arquitectónicas

## ADR-001 - Strategy para algoritmos de navegación
Se encapsulan A* y Dijkstra detrás de `RouteStrategy`. La decisión evita condicionales dispersos, permite pruebas comparativas y facilita incorporar nuevas estrategias.

## ADR-002 - A* como estrategia optimizada predeterminada
Para mapas de cuadrícula con costo uniforme se utiliza distancia Manhattan como heurística admisible. En el benchmark de laboratorio A* mantuvo el mismo costo de ruta que Dijkstra y redujo nodos explorados entre 63.81 % y 67.13 %.

## ADR-003 - Command en el límite de aplicación
`CalculateRouteCommand` encapsula parámetros y ejecución del caso de uso. Esto desacopla la API del servicio y permite reutilizar la acción desde otros adaptadores.

## ADR-004 - Observer para métricas
La instrumentación se separa de la lógica algorítmica. `MetricsObserver` recibe el resultado del cálculo sin que los algoritmos conozcan detalles de observabilidad.
