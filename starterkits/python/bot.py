from game_message import *
import itertools
from collections import deque


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: TeamGameState):
        actions = []
        remaining = game_message.maximumNumberOfBiomassPerTurn
        available = game_message.availableBiomass
        grid = game_message.map.biomass

        # --- 1️ Lister toutes les paires de colonies ---
        colonies = game_message.map.colonies
        pairs = list(itertools.combinations(colonies, 2))

        # --- 2 Trouver les plus courts chemins ---
        paths = []
        for c1, c2 in pairs:
            path = self.find_shortest_path(c1.position, c2.position, grid, game_message)
            if path:
                distance = len(path)
                min_value = min(c1.nutrients, c2.nutrients)
                paths.append((distance, -min_value, path, min_value))

        # --- 3️ Trier les chemins (plus court puis plus rentable) ---
        paths.sort(key=lambda x: (x[0], x[1]))

        print("Chemins: ", paths)

        # --- 4️ Remplir de biomasse chemin par chemin ---
        for _, _, path, max_biomass in paths:
            for pos in path[1:-1]:  # Exclure les colonies de début et de fin
                if remaining <= 0 or available <= 0:
                    break

                current = grid[pos.x][pos.y]
                if current < max_biomass:
                    add_amount = min(max_biomass - current, remaining, available)
                    if add_amount > 0:
                        actions.append(AddBiomassAction(position=pos, amount=add_amount))
                        remaining -= add_amount
                        available -= add_amount

            if remaining <= 0 or available <= 0:
                break

        return actions

    # --- Trouve le plus court chemin entre deux positions (BFS) ---
    # path = (distance, -min_value, path, min_value)
    def find_shortest_path(self, start, end, grid, game_message):
        """
        Trouve le plus court chemin entre deux positions (BFS),
        en évitant les colonies (sauf départ et arrivée).
        """
        width, height = game_message.map.width, game_message.map.height
        colonies_positions = {(c.position.x, c.position.y) for c in game_message.map.colonies}

        visited = set()
        queue = deque([(start, [start])])

        while queue:
            pos, path = queue.popleft()
            if (pos.x, pos.y) in visited:
                continue
            visited.add((pos.x, pos.y))

            # Si on atteint la colonie d'arrivée -> chemin trouvé
            if pos.x == end.x and pos.y == end.y:
                return path

            # Explore les 4 directions (haut, bas, gauche, droite)
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = pos.x + dx, pos.y + dy

                # Vérifie que la position est dans la carte
                if not (0 <= nx < width and 0 <= ny < height):
                    continue

                # Interdit de passer sur une colonie sauf start ou end
                if (nx, ny) in colonies_positions and (nx, ny) not in [(start.x, start.y), (end.x, end.y)]:
                    continue

                # Si tout est bon, on ajoute à la file
                next_pos = Position(nx, ny)
                queue.append((next_pos, path + [next_pos]))

        # Aucun chemin trouvé
        return None