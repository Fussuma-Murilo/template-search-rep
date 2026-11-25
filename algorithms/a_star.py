import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        total = 0
        for index, tile in enumerate(state.tiles):
            if tile != 0:
                row, col = divmod(index, 3)
                goal_row, goal_col = divmod(tile - 1, 3)
                total += abs(row - goal_row) + abs(col - goal_col)
        return total

    def search(self, initial: State) -> SearchResult:
        frontier = [(initial.cost + self.heuristic(initial), 0, initial)]
        best_cost = {initial: initial.cost}
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            _, _, state = heapq.heappop(frontier)
            if state.cost > best_cost[state]:
                continue
            if state.is_goal:
                result.solution = state
                result.depth = state.cost - initial.cost
                break

            result.nodes_expanded += 1
            for child in state.neighbors():
                result.nodes_generated += 1
                if child not in best_cost or child.cost < best_cost[child]:
                    best_cost[child] = child.cost
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, result.nodes_generated, child))
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
