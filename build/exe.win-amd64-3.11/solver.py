import heapq
# se usa para manejar la cola de prioridad del algoritmo A*.

class Solver:
    def solve(self, level):
        start_state = self.get_state(level)
        # Obtiene el estado inicial del nivel, que incluye la posición del jugador y las cajas.
        goal_state = frozenset(level.targets)
        # Define el estado objetivo como las posiciones objetivo para las cajas.

        frontier = [(0, start_state)]
        # Inicializa la cola de prioridad con el estado inicial, con costo 0.
        came_from = {}
        # Almacena de dónde vino cada estado para reconstruir el camino.
        cost_so_far = {start_state: 0}
        # Almacena el costo acumulado para llegar a cada estado.

        while frontier:
            current_cost, current_state = heapq.heappop(frontier)
            # Extrae el estado con la prioridad más baja de la cola.

            if self.is_goal(current_state, goal_state):
                return self.reconstruct_path(came_from, start_state, current_state)
                # Si se alcanza el estado objetivo, reconstruye y devuelve el camino.

            for next_state in self.get_neighbors(current_state, level):
                # Itera sobre los estados vecinos posibles desde el estado actual.
                new_cost = cost_so_far[current_state] + 1
                # Calcula el nuevo costo para llegar al vecino.

                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    # Actualiza si el vecino no ha sido visitado o si se encuentra un costo menor.
                    cost_so_far[next_state] = new_cost
                    priority = new_cost + self.heuristic(next_state, goal_state)
                    # Calcula la prioridad combinando el costo y la heurística.
                    heapq.heappush(frontier, (priority, next_state))
                    # Añade el vecino a la cola de prioridad.
                    came_from[next_state] = current_state
                    # Registra de dónde se llegó a este vecino.

        return None
        # Devuelve `None` si no encuentra una solución.

    def get_state(self, level):
        # Representa el estado como la posición del jugador y las cajas.
        return (level.player_pos[0], level.player_pos[1], frozenset(level.boxes))

    def is_goal(self, state, goal_state):
        # Comprueba si todas las cajas están en las posiciones objetivo.
        return state[2] == goal_state

    def get_neighbors(self, state, level):
        # Genera los estados vecinos válidos desde el estado actual.
        x, y, boxes = state
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            # Intenta mover al jugador en las cuatro direcciones posibles.
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) in level.walls:
                continue
                # Salta si el jugador se mueve hacia una pared.

            if (new_x, new_y) in boxes:
                # Si el jugador intenta empujar una caja:
                push_x, push_y = new_x + dx, new_y + dy
                # Calcula la nueva posición de la caja.
                if (push_x, push_y) not in level.walls and (push_x, push_y) not in boxes:
                    # Solo permite mover la caja si el espacio está libre.
                    new_boxes = frozenset(b if b != (new_x, new_y) else (push_x, push_y) for b in boxes)
                    neighbors.append((new_x, new_y, new_boxes))
                    # Añade el estado con la nueva posición de la caja.
            else:
                neighbors.append((new_x, new_y, boxes))
                # Si no hay caja, simplemente mueve al jugador.

        return neighbors

    def heuristic(self, state, goal_state):
        # Calcula la heurística basada en la distancia de Manhattan de cada caja al objetivo más cercano.
        _, _, boxes = state
        return sum(min(abs(bx - gx) + abs(by - gy) for gx, gy in goal_state) for bx, by in boxes)

    def reconstruct_path(self, came_from, start, goal):
        # Reconstruye el camino desde el estado inicial al estado objetivo.
        current = goal
        path = []
        while current != start:
            prev = came_from[current]
            # Retrocede al estado anterior.
            dx, dy = current[0] - prev[0], current[1] - prev[1]
            # Calcula el movimiento realizado.
            path.append((dx, dy))
            current = prev
        path.reverse()
        # Invierte el camino para que esté en el orden correcto.
        return path
