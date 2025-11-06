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

        # --- 1️⃣ Lister toutes les paires de colonies ---
        colonies = game_message.map.colonies
        pairs = list(itertools.combinations(colonies, 2))

        # --- 2️⃣ Trouver les plus courts chemins ---
        paths = []
        for c1, c2 in pairs:
            path = self.find_shortest_path(c1.position, c2.position, grid, game_message)
            if path:
                distance = len(path)
                min_value = min(c1.nutrients, c2.nutrients)
                paths.append((distance, -min_value, path, min_value))

        # --- 3️⃣ Trier les chemins (plus court puis plus rentable) ---
        paths.sort(key=lambda x: (x[0], x[1]))

        # --- 4️⃣ Remplir de biomasse chemin par chemin ---
        for _, _, path, max_biomass in paths:
            for pos in path:
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
    def find_shortest_path(self, start, end, grid, game_message):
        width, height = game_message.map.width, game_message.map.height
        visited = set()
        queue = deque([(start, [start])])

        while queue:
            pos, path = queue.popleft()
            if (pos.x, pos.y) in visited:
                continue
            visited.add((pos.x, pos.y))

            if pos.x == end.x and pos.y == end.y:
                return path

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = pos.x + dx, pos.y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    queue.append((Position(nx, ny), path + [Position(nx, ny)]))

        return None