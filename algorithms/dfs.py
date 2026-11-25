from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        best_depth = {initial: 0}
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            state = frontier.pop()
            depth = state.cost - initial.cost
            if depth > best_depth[state]:
                continue
            if state.is_goal:
                result.solution = state
                result.depth = depth
                break
            if depth >= self.depth_limit:
                continue

            result.nodes_expanded += 1
            for child in reversed(state.neighbors()):
                result.nodes_generated += 1
                child_depth = depth + 1
                if child not in best_depth or child_depth < best_depth[child]:
                    best_depth[child] = child_depth
                    frontier.append(child)
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
