"""Sections 13 and 14."""

G_EDGES = [[0, 1], [0, 2], [1, 2], [1, 3]]
W_EDGES = [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]]


def register(add):
    extra = {"nodes": [0, 1, 2, 3], "edges": G_EDGES}
    wextra = {"nodes": [0, 1, 2, 3], "edges": W_EDGES}

    add("topic-13-1", "Adjacency lists", "graph", ["graph", "e"],
        "Build an undirected adjacency list from edges and return graph[0], graph[1], graph[2], graph[3] as one list of lists. Neighbors stay in insertion order.",
        "A graph in memory is a list of neighbor lists. Each edge writes the connection into both endpoints.",
        ["Start an empty list per node.", "Append each edge both ways.", "Return the four neighbor lists."],
        "Undirected adjacency lists.",
        """
        def solve(n, edges):
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])
            return graph
        """,
        ["solve(4, [[0, 1], [0, 2], [1, 2], [1, 3]])", "solve(1, [])", "solve(2, [[0, 1]])"],
        expect=[[[1, 2], [0, 2, 3], [0, 1], [1]], [[]], [[1], [0]]],
        extra=extra)

    add("topic-13-2", "BFS order", "graph", ["graph", "q", "seen", "order", "node"],
        "Return the BFS visit order from node 0. Neighbors are tried in increasing id.",
        "BFS stores the frontier in a queue. The node that leaves the queue is the one whose neighbors get stored next.",
        ["Start the queue with 0.", "Pop the front and record it.", "Push unseen neighbors."],
        "Queue BFS from 0.",
        """
        def solve(n, edges):
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])
            for row in graph:
                row.sort()
            q = [0]
            seen = [0]
            order = []
            while q:
                node = q.pop(0)
                order.append(node)
                for nxt in graph[node]:
                    if nxt not in seen:
                        seen.append(nxt)
                        q.append(nxt)
            return order
        """,
        ["solve(4, [[0, 1], [0, 2], [1, 2], [1, 3]])", "solve(1, [])", "solve(2, [[0, 1]])"],
        expect=[[0, 1, 2, 3], [0], [0, 1]],
        extra=extra)

    add("topic-13-3", "DFS order", "graph", ["graph", "seen", "order", "node"],
        "Return the DFS visit order from node 0. Neighbors are tried in increasing id.",
        "DFS stores the path in the call stack. A node is recorded when the call starts, then each neighbor gets its own call.",
        ["Mark the node seen and record it.", "Call each unseen neighbor.", "The stack shrinks when a branch ends."],
        "Recursive DFS from 0.",
        """
        def solve(n, edges):
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])
            for row in graph:
                row.sort()
            seen = []
            order = []

            def dfs(node):
                seen.append(node)
                order.append(node)
                for nxt in graph[node]:
                    if nxt not in seen:
                        dfs(nxt)

            dfs(0)
            return order
        """,
        ["solve(4, [[0, 1], [0, 2], [1, 2], [1, 3]])", "solve(1, [])", "solve(2, [[1, 0]])"],
        expect=[[0, 1, 2, 3], [0], [0, 1]],
        extra=extra)

    add("topic-13-4", "Kahn order", "graph", ["indeg", "q", "order", "node"],
        "edges are directed [u, v] meaning u must come before v. Return a topological order using Kahn's algorithm. When several nodes are ready, take the smaller id first.",
        "Kahn's algorithm stores indegrees and a queue of nodes whose indegree is already 0. Each pop writes that node into the order and frees its neighbors.",
        ["Count incoming edges.", "Queue every node with count 0.", "Pop, append to the order, and decrease neighbors."],
        "Kahn topological sort.",
        """
        def solve(n, edges):
            graph = []
            indeg = []
            i = 0
            while i < n:
                graph.append([])
                indeg.append(0)
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                indeg[e[1]] = indeg[e[1]] + 1
            q = []
            i = 0
            while i < n:
                if indeg[i] == 0:
                    q.append(i)
                i = i + 1
            order = []
            while q:
                q.sort()
                node = q.pop(0)
                order.append(node)
                for nxt in graph[node]:
                    indeg[nxt] = indeg[nxt] - 1
                    if indeg[nxt] == 0:
                        q.append(nxt)
            return order
        """,
        ["solve(4, [[0, 1], [0, 2], [1, 3]])", "solve(1, [])", "solve(2, [[0, 1]])"],
        expect=[[0, 1, 2, 3], [0], [0, 1]],
        extra={"nodes": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [1, 3]]})

    add("topic-13-5", "Shortest paths", "graph", ["dist", "heap", "u"],
        "Undirected weighted edges are [u, v, w]. Return the Dijkstra distances from 0. Unreachable nodes stay 10**9.",
        "Dijkstra stores the best known distance. A heap always offers the closest unsettled node next.",
        ["dist[0] starts at 0.", "Pop the closest node.", "Relax each neighbor if the path is shorter."],
        "Dijkstra with a heap.",
        """
        def solve(n, edges):
            import heapq
            graph = []
            dist = []
            i = 0
            while i < n:
                graph.append([])
                dist.append(10 ** 9)
                i = i + 1
            for e in edges:
                graph[e[0]].append([e[1], e[2]])
                graph[e[1]].append([e[0], e[2]])
            dist[0] = 0
            heap = [(0, 0)]
            while heap:
                cost, u = heapq.heappop(heap)
                if cost != dist[u]:
                    continue
                for nxt in graph[u]:
                    v = nxt[0]
                    w = nxt[1]
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        heapq.heappush(heap, (dist[v], v))
            return dist
        """,
        ["solve(4, [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]])", "solve(1, [])", "solve(2, [[0, 1, 5]])"],
        expect=[[0, 1, 3, 6], [0], [0, 5]],
        extra=wextra)

    add("topic-13-6", "Relax every edge", "graph", ["dist", "e", "round"],
        "Directed edges [u, v, w] may be negative but have no negative cycle. Return Bellman-Ford distances from 0. Unreachable stays 10**9.",
        "Bellman-Ford stores a distance per node and relaxes every edge once per round. After n-1 rounds, every simple path has been considered.",
        ["Set dist[0] to 0.", "Repeat n - 1 rounds.", "Relax every edge in each round."],
        "Bellman-Ford.",
        """
        def solve(n, edges):
            dist = []
            i = 0
            while i < n:
                dist.append(10 ** 9)
                i = i + 1
            dist[0] = 0
            round = 0
            while round < n - 1:
                for e in edges:
                    if dist[e[0]] < 10 ** 9 and dist[e[0]] + e[2] < dist[e[1]]:
                        dist[e[1]] = dist[e[0]] + e[2]
                round = round + 1
            return dist
        """,
        ["solve(4, [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]])", "solve(1, [])", "solve(3, [[0, 1, 2], [1, 2, -3]])"],
        expect=[[0, 1, 3, 6], [0], [0, 2, -1]],
        extra=wextra)

    add("topic-13-7", "All pairs", "matrix", ["dist", "k", "i", "j"],
        "Undirected weighted edges. Return the Floyd-Warshall distance matrix. Use 10**9 for a missing edge before the algorithm fills it.",
        "Floyd-Warshall stores every pair distance in a matrix. For each intermediate k it asks whether i -> k -> j is shorter than the stored i -> j.",
        ["Seed the matrix with edge weights.", "Try every intermediate k.", "Write a shorter path into dist[i][j]."],
        "Floyd-Warshall.",
        """
        def solve(n, edges):
            inf = 10 ** 9
            dist = []
            i = 0
            while i < n:
                row = []
                j = 0
                while j < n:
                    if i == j:
                        row.append(0)
                    else:
                        row.append(inf)
                    j = j + 1
                dist.append(row)
                i = i + 1
            for e in edges:
                if e[2] < dist[e[0]][e[1]]:
                    dist[e[0]][e[1]] = e[2]
                    dist[e[1]][e[0]] = e[2]
            k = 0
            while k < n:
                i = 0
                while i < n:
                    j = 0
                    while j < n:
                        if dist[i][k] + dist[k][j] < dist[i][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                        j = j + 1
                    i = i + 1
                k = k + 1
            return dist
        """,
        ["solve(4, [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]])", "solve(1, [])"],
        expect=[[[0, 1, 3, 6], [1, 0, 2, 5], [3, 2, 0, 3], [6, 5, 3, 0]], [[0]]])

    add("topic-13-8", "Prim weight", "graph", ["in_tree", "best", "total"],
        "Return the total weight of a minimum spanning tree. The graph is connected and undirected.",
        "Prim grows one stored set of nodes. best[v] is the cheapest edge that reaches v from that set.",
        ["Start with node 0 inside the tree.", "Pick the outside node with the smallest best edge.", "Update its neighbors."],
        "Prim's algorithm. Return the total weight.",
        """
        def solve(n, edges):
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append([e[1], e[2]])
                graph[e[1]].append([e[0], e[2]])
            in_tree = []
            best = []
            i = 0
            while i < n:
                in_tree.append(False)
                best.append(10 ** 9)
                i = i + 1
            best[0] = 0
            total = 0
            taken = 0
            while taken < n:
                u = -1
                i = 0
                while i < n:
                    if not in_tree[i] and (u == -1 or best[i] < best[u]):
                        u = i
                    i = i + 1
                in_tree[u] = True
                total = total + best[u]
                taken = taken + 1
                for nxt in graph[u]:
                    if not in_tree[nxt[0]] and nxt[1] < best[nxt[0]]:
                        best[nxt[0]] = nxt[1]
            return total
        """,
        ["solve(4, [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]])", "solve(1, [])", "solve(2, [[0, 1, 5]])"],
        expect=[6, 0, 5],
        extra=wextra)

    add("topic-13-9", "Kruskal weight", "array", ["edges", "parent", "total"],
        "Return the MST weight using Kruskal: sort edges, then add an edge when its ends are in different union-find sets.",
        "Kruskal stores components. An edge merges two components only when find says they differ. That rule blocks cycles.",
        ["Sort edges by weight.", "Unite the ends when they differ.", "Add the weight when a unite succeeds."],
        "Kruskal with union-find.",
        """
        def solve(n, edges):
            parent = []
            i = 0
            while i < n:
                parent.append(i)
                i = i + 1

            def find(x):
                while parent[x] != x:
                    x = parent[x]
                return x

            ordered = sorted(edges, key=lambda e: e[2])
            total = 0
            for e in ordered:
                a = find(e[0])
                b = find(e[1])
                if a != b:
                    parent[b] = a
                    total = total + e[2]
            return total
        """,
        ["solve(4, [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]])", "solve(1, [])", "solve(2, [[0, 1, 5]])"],
        expect=[6, 0, 5])

    add("topic-13-10", "Component count", "array", ["parent", "e"],
        "Unite each undirected edge. Return how many components remain.",
        "Union-find stores a parent for each node. Uniting two roots links one component under the other. A node whose parent is itself is still a root.",
        ["Start each node as its own parent.", "Unite the two ends of every edge.", "Count the roots."],
        "Union-find, then count roots.",
        """
        def solve(n, edges):
            parent = []
            i = 0
            while i < n:
                parent.append(i)
                i = i + 1

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            for e in edges:
                a = find(e[0])
                b = find(e[1])
                if a != b:
                    parent[b] = a
            roots = 0
            i = 0
            while i < n:
                if find(i) == i:
                    roots = roots + 1
                i = i + 1
            return roots
        """,
        ["solve(4, [[0, 1], [1, 2]])", "solve(3, [])", "solve(2, [[0, 1]])"],
        expect=[2, 3, 1])

    add("topic-13-11", "Bridge edges", "graph", ["tin", "low", "bridges", "u"],
        "Return the bridges of an undirected graph as sorted [smaller, larger] pairs. A bridge is an edge whose removal disconnects the graph.",
        "Discovery time and low-link live on each node. An edge u-v is a bridge when v cannot climb back to u or above.",
        ["DFS and store the enter time.", "low[v] is the smallest time reachable from v.", "Record the edge when low[v] is greater than tin[u]."],
        "Tarjan-style bridge search.",
        """
        def solve(n, edges):
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])
            tin = []
            low = []
            i = 0
            while i < n:
                tin.append(-1)
                low.append(-1)
                i = i + 1
            bridges = []
            clock = [0]

            def dfs(u, parent):
                tin[u] = clock[0]
                low[u] = clock[0]
                clock[0] = clock[0] + 1
                for v in graph[u]:
                    if v == parent:
                        continue
                    if tin[v] == -1:
                        dfs(v, u)
                        if low[v] < low[u]:
                            low[u] = low[v]
                        if low[v] > tin[u]:
                            if u < v:
                                bridges.append([u, v])
                            else:
                                bridges.append([v, u])
                    elif tin[v] < low[u]:
                        low[u] = tin[v]

            i = 0
            while i < n:
                if tin[i] == -1:
                    dfs(i, -1)
                i = i + 1
            bridges.sort()
            return bridges
        """,
        ["solve(4, [[0, 1], [1, 2], [1, 3]])", "solve(3, [[0, 1], [1, 2], [2, 0]])", "solve(1, [])"],
        expect=[[[0, 1], [1, 2], [1, 3]], [], []],
        extra={"nodes": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [1, 3]]})

    add("topic-13-12", "Cut vertices", "graph", ["tin", "low", "cuts", "u"],
        "Return the articulation points in increasing order.",
        "A cut vertex is stored when a child cannot reach above it, or when the root has two separate DFS children.",
        ["Record discovery times.", "A non-root is a cut if some child has low >= tin[u].", "The root is a cut when it has two or more DFS children."],
        "Find articulation points.",
        """
        def solve(n, edges):
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])
            tin = []
            low = []
            i = 0
            while i < n:
                tin.append(-1)
                low.append(-1)
                i = i + 1
            cuts = []
            clock = [0]

            def dfs(u, parent):
                tin[u] = clock[0]
                low[u] = clock[0]
                clock[0] = clock[0] + 1
                children = 0
                is_cut = False
                for v in graph[u]:
                    if v == parent:
                        continue
                    if tin[v] == -1:
                        children = children + 1
                        dfs(v, u)
                        if low[v] < low[u]:
                            low[u] = low[v]
                        if parent != -1 and low[v] >= tin[u]:
                            is_cut = True
                    elif tin[v] < low[u]:
                        low[u] = tin[v]
                if parent == -1 and children > 1:
                    is_cut = True
                if is_cut:
                    cuts.append(u)

            i = 0
            while i < n:
                if tin[i] == -1:
                    dfs(i, -1)
                i = i + 1
            cuts.sort()
            return cuts
        """,
        ["solve(4, [[0, 1], [1, 2], [1, 3]])", "solve(3, [[0, 1], [1, 2], [2, 0]])", "solve(2, [[0, 1]])"],
        expect=[[1], [], []],
        extra={"nodes": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [1, 3]]})

    add("topic-13-13", "Two colors", "graph", ["color", "q", "node"],
        "Return True when the undirected graph is bipartite.",
        "A bipartite graph can be stored as two colors. BFS colors a neighbor with the opposite color and fails if a neighbor is already the same color.",
        ["Color the start node 0.", "Color each neighbor 1 - color[node].", "Return False on a clash."],
        "BFS 2-coloring.",
        """
        def solve(n, edges):
            graph = []
            color = []
            i = 0
            while i < n:
                graph.append([])
                color.append(-1)
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])
            i = 0
            while i < n:
                if color[i] == -1:
                    color[i] = 0
                    q = [i]
                    while q:
                        node = q.pop(0)
                        for nxt in graph[node]:
                            if color[nxt] == -1:
                                color[nxt] = 1 - color[node]
                                q.append(nxt)
                            elif color[nxt] == color[node]:
                                return False
                i = i + 1
            return True
        """,
        ["solve(3, [[0, 1], [1, 2]])", "solve(3, [[0, 1], [1, 2], [2, 0]])", "solve(1, [])"],
        expect=[True, False, True],
        extra={"nodes": [0, 1, 2], "edges": [[0, 1], [1, 2]]})

    add("topic-13-14", "Euler path exists", "graph", ["deg", "e"],
        "Return True when the undirected graph has an Eulerian path: it is connected (ignoring isolated nodes) and has 0 or 2 odd degrees.",
        "An Eulerian path uses every edge once. The degree list is the memory that decides it: zero or two odds, and one non-isolated component.",
        ["Count degrees.", "Count odd degrees.", "Check that the non-isolated nodes are one connected piece."],
        "Degree check plus a connectivity walk.",
        """
        def solve(n, edges):
            graph = []
            deg = []
            i = 0
            while i < n:
                graph.append([])
                deg.append(0)
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])
                deg[e[0]] = deg[e[0]] + 1
                deg[e[1]] = deg[e[1]] + 1
            odds = 0
            start = -1
            i = 0
            while i < n:
                if deg[i] % 2 == 1:
                    odds = odds + 1
                if deg[i] > 0 and start == -1:
                    start = i
                i = i + 1
            if odds != 0 and odds != 2:
                return False
            if start == -1:
                return True
            seen = []
            stack = [start]
            while stack:
                node = stack.pop()
                if node in seen:
                    continue
                seen.append(node)
                for nxt in graph[node]:
                    stack.append(nxt)
            i = 0
            while i < n:
                if deg[i] > 0 and i not in seen:
                    return False
                i = i + 1
            return True
        """,
        ["solve(3, [[0, 1], [1, 2]])", "solve(3, [[0, 1], [1, 2], [2, 0]])", "solve(4, [[0, 1], [2, 3]])"],
        expect=[True, True, False])

    add("topic-13-15", "Visit once", "graph", ["path", "used"],
        "n is at most 4. Return True when some path visits every node exactly once.",
        "A Hamiltonian path is a permutation of the nodes where every consecutive pair is an edge. The used list stores who is already on the path.",
        ["Start at each node.", "Append an unused neighbor.", "Succeed when the path length is n."],
        "Backtrack over unused neighbors.",
        """
        def solve(n, edges):
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append(e[1])
                graph[e[1]].append(e[0])

            def walk(node, used):
                if len(used) == n:
                    return True
                for nxt in graph[node]:
                    if nxt not in used:
                        used.append(nxt)
                        if walk(nxt, used):
                            return True
                        used.pop()
                return False

            start = 0
            while start < n:
                if walk(start, [start]):
                    return True
                start = start + 1
            return False
        """,
        ["solve(4, [[0, 1], [1, 2], [2, 3]])", "solve(3, [[0, 1]])", "solve(1, [])"],
        expect=[True, False, True])

    add("topic-13-16", "Max flow", "graph", ["cap", "parent", "flow"],
        "cap_edges are directed [u, v, capacity]. Return the maximum flow from 0 to n-1.",
        "Flow stores residual capacity. An augmenting path is a route with leftover capacity. Sending the bottleneck along it updates those residuals.",
        ["BFS a path in the residual graph.", "The bottleneck is the smallest residual on it.", "Subtract it forward and add it backward."],
        "Edmonds-Karp max flow.",
        """
        def solve(n, cap_edges):
            cap = []
            i = 0
            while i < n:
                row = []
                j = 0
                while j < n:
                    row.append(0)
                    j = j + 1
                cap.append(row)
                i = i + 1
            for e in cap_edges:
                cap[e[0]][e[1]] = cap[e[0]][e[1]] + e[2]
            flow = 0
            while True:
                parent = []
                i = 0
                while i < n:
                    parent.append(-1)
                    i = i + 1
                parent[0] = -2
                q = [0]
                while q and parent[n - 1] == -1:
                    u = q.pop(0)
                    v = 0
                    while v < n:
                        if parent[v] == -1 and cap[u][v] > 0:
                            parent[v] = u
                            q.append(v)
                        v = v + 1
                if parent[n - 1] == -1:
                    return flow
                bottleneck = 10 ** 9
                v = n - 1
                while v != 0:
                    u = parent[v]
                    if cap[u][v] < bottleneck:
                        bottleneck = cap[u][v]
                    v = u
                v = n - 1
                while v != 0:
                    u = parent[v]
                    cap[u][v] = cap[u][v] - bottleneck
                    cap[v][u] = cap[v][u] + bottleneck
                    v = u
                flow = flow + bottleneck
        """,
        ["solve(4, [[0, 1, 3], [0, 2, 2], [1, 3, 2], [2, 3, 3]])", "solve(2, [[0, 1, 5]])", "solve(2, [])"],
        expect=[4, 5, 0],
        extra={"nodes": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [1, 3], [2, 3]]})

    add("topic-13-17", "Shortest augmenting path", "graph", ["cap", "flow"],
        "Same network as a capacity list. Return the max flow. Each augmenting path is a BFS path, which is what Edmonds-Karp chooses.",
        "Edmonds-Karp always augments along a residual path with the fewest edges. The queue builds that shortest path.",
        ["BFS from the source in the residual graph.", "Add the bottleneck to the flow.", "Stop when the sink is unreachable."],
        "BFS augmenting paths.",
        """
        def solve(n, cap_edges):
            cap = []
            i = 0
            while i < n:
                row = []
                j = 0
                while j < n:
                    row.append(0)
                    j = j + 1
                cap.append(row)
                i = i + 1
            for e in cap_edges:
                cap[e[0]][e[1]] = cap[e[0]][e[1]] + e[2]
            flow = 0
            sink = n - 1
            while True:
                parent = []
                i = 0
                while i < n:
                    parent.append(-1)
                    i = i + 1
                parent[0] = -2
                q = [0]
                while q and parent[sink] == -1:
                    u = q.pop(0)
                    v = 0
                    while v < n:
                        if parent[v] == -1 and cap[u][v] > 0:
                            parent[v] = u
                            q.append(v)
                        v = v + 1
                if parent[sink] == -1:
                    return flow
                add = 10 ** 9
                v = sink
                while v != 0:
                    if cap[parent[v]][v] < add:
                        add = cap[parent[v]][v]
                    v = parent[v]
                v = sink
                while v != 0:
                    u = parent[v]
                    cap[u][v] = cap[u][v] - add
                    cap[v][u] = cap[v][u] + add
                    v = u
                flow = flow + add
        """,
        ["solve(4, [[0, 1, 3], [0, 2, 2], [1, 3, 2], [2, 3, 3]])", "solve(2, [[0, 1, 4]])", "solve(2, [])"],
        expect=[4, 4, 0])

    add("topic-13-18", "First level graph", "graph", ["level", "q", "node"],
        "Dinic starts by layering the residual graph with a BFS. On the original capacities, return the level of each node from the source 0. Unreachable is -1.",
        "A level is the fewest residual edges from the source. Dinic only sends flow along edges that climb exactly one level.",
        ["level[0] = 0.", "BFS assigns level[child] = level[node] + 1.", "Nodes never reached stay -1."],
        "BFS levels from 0.",
        """
        def solve(n, cap_edges):
            graph = []
            level = []
            i = 0
            while i < n:
                graph.append([])
                level.append(-1)
                i = i + 1
            for e in cap_edges:
                if e[2] > 0:
                    graph[e[0]].append(e[1])
            level[0] = 0
            q = [0]
            while q:
                node = q.pop(0)
                for nxt in graph[node]:
                    if level[nxt] == -1:
                        level[nxt] = level[node] + 1
                        q.append(nxt)
            return level
        """,
        ["solve(4, [[0, 1, 3], [0, 2, 2], [1, 3, 2], [2, 3, 3]])", "solve(2, [])", "solve(1, [])"],
        expect=[[0, 1, 1, 2], [0, -1], [0]],
        extra={"nodes": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [1, 3], [2, 3]]})

    add("topic-13-19", "From every source", "matrix", ["dist", "src"],
        "Non-negative undirected weights. Johnson's algorithm becomes Dijkstra from every node when no reweighting is needed. Return the distance matrix.",
        "Each row is one Dijkstra. dist[src][v] is the best distance stored for that source.",
        ["For each source, reset distances.", "Relax with a heap.", "Return every row."],
        "Dijkstra from every node.",
        """
        def solve(n, edges):
            import heapq
            graph = []
            i = 0
            while i < n:
                graph.append([])
                i = i + 1
            for e in edges:
                graph[e[0]].append([e[1], e[2]])
                graph[e[1]].append([e[0], e[2]])
            dist = []
            src = 0
            while src < n:
                row = []
                i = 0
                while i < n:
                    row.append(10 ** 9)
                    i = i + 1
                row[src] = 0
                heap = [(0, src)]
                while heap:
                    cost, u = heapq.heappop(heap)
                    if cost != row[u]:
                        continue
                    for nxt in graph[u]:
                        if row[u] + nxt[1] < row[nxt[0]]:
                            row[nxt[0]] = row[u] + nxt[1]
                            heapq.heappush(heap, (row[nxt[0]], nxt[0]))
                dist.append(row)
                src = src + 1
            return dist
        """,
        ["solve(4, [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]])", "solve(1, [])"],
        expect=[[[0, 1, 3, 6], [1, 0, 2, 5], [3, 2, 0, 3], [6, 5, 3, 0]], [[0]]])

    add("topic-13-20", "Zero-one edges", "graph", ["dist", "dq", "u"],
        "Edges are [u, v, w] with w equal to 0 or 1, directed. Return distances from 0. Unreachable stays 10**9.",
        "0-1 BFS uses a deque. A 0-weight edge is pushed at the front because it does not increase the distance. A 1-weight edge goes to the back.",
        ["dist[0] = 0 and the deque holds 0.", "Relax a neighbor.", "Push front for weight 0, back for weight 1."],
        "0-1 BFS.",
        """
        def solve(n, edges):
            graph = []
            dist = []
            i = 0
            while i < n:
                graph.append([])
                dist.append(10 ** 9)
                i = i + 1
            for e in edges:
                graph[e[0]].append([e[1], e[2]])
            dist[0] = 0
            dq = [0]
            while dq:
                u = dq.pop(0)
                for nxt in graph[u]:
                    v = nxt[0]
                    w = nxt[1]
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        if w == 0:
                            dq.insert(0, v)
                        else:
                            dq.append(v)
            return dist
        """,
        ["solve(4, [[0, 1, 0], [0, 2, 1], [1, 3, 1], [2, 3, 0]])", "solve(1, [])", "solve(2, [[0, 1, 0]])"],
        expect=[[0, 0, 1, 1], [0], [0, 0]],
        extra={"nodes": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [1, 3], [2, 3]]})

    add("topic-13-21", "A satisfying assignment", "flow", ["mask", "ok", "clause"],
        "There are 2 variables, numbered 1 and 2. A clause is a list of literals; negative means NOT. Return the first bitmask assignment [x1, x2] in order 00, 01, 10, 11 that satisfies every clause, or None.",
        "2-SAT assignments are bits. This scan stores one mask and tests every literal. The first mask that makes every clause true is the output.",
        ["Try mask from 0 to 3.", "A clause is true if any literal matches the bit.", "Return the bits of the first success."],
        "Try all 4 assignments.",
        """
        def solve(clauses):
            mask = 0
            while mask < 4:
                ok = True
                for clause in clauses:
                    good = False
                    for lit in clause:
                        var = abs(lit) - 1
                        bit = (mask >> var) & 1
                        if lit > 0 and bit == 1:
                            good = True
                        if lit < 0 and bit == 0:
                            good = True
                    if not good:
                        ok = False
                if ok:
                    return [mask & 1, (mask >> 1) & 1]
                mask = mask + 1
            return None
        """,
        ["solve([[1, 1], [2, 2]])", "solve([[1, -1]])", "solve([[1], [-1]])"],
        expect=[[1, 1], [0, 0], None])

    add("topic-13-22", "Stable pairs", "array", ["men", "women", "next_choice", "wife"],
        "Two men and two women. men[m] and women[w] are preference lists, most preferred first. Return the woman index matched to each man by Gale-Shapley, men proposing.",
        "Gale-Shapley stores each man's next proposal and each woman's current partner. A woman replaces her partner only when the new man ranks higher.",
        ["A free man proposes to his next woman.", "She accepts if she is free or prefers him.", "The dumped man becomes free."],
        "Men propose in order.",
        """
        def solve(men, women):
            n = len(men)
            rank = []
            w = 0
            while w < n:
                row = []
                i = 0
                while i < n:
                    row.append(0)
                    i = i + 1
                p = 0
                while p < n:
                    row[women[w][p]] = p
                    p = p + 1
                rank.append(row)
                w = w + 1
            next_choice = []
            wife = []
            husband = []
            free = []
            i = 0
            while i < n:
                next_choice.append(0)
                wife.append(-1)
                husband.append(-1)
                free.append(i)
                i = i + 1
            while free:
                m = free.pop(0)
                w = men[m][next_choice[m]]
                next_choice[m] = next_choice[m] + 1
                if husband[w] == -1:
                    husband[w] = m
                    wife[m] = w
                elif rank[w][m] < rank[w][husband[w]]:
                    old = husband[w]
                    wife[old] = -1
                    free.append(old)
                    husband[w] = m
                    wife[m] = w
                else:
                    free.append(m)
            return wife
        """,
        ["solve([[0, 1], [0, 1]], [[1, 0], [0, 1]])", "solve([[0, 1], [1, 0]], [[0, 1], [0, 1]])"],
        expect=[[1, 0], [0, 1]])

    add("topic-14-1", "Recursive sum", "recursion", ["nums", "i", "rest"],
        "Return the sum of nums using recursion on the index, not a loop.",
        "Each call stores its index. The return value is nums[i] plus whatever the next call returns.",
        ["Past the end, return 0.", "Ask for the sum of the suffix.", "Add nums[i] on the way back."],
        "solve_from(i) = nums[i] + solve_from(i + 1).",
        """
        def solve(nums):
            def walk(i):
                if i == len(nums):
                    return 0
                rest = walk(i + 1)
                return nums[i] + rest
            return walk(0)
        """,
        ["solve([2, 4, 6])", "solve([])", "solve([5])"],
        expect=[12, 0, 5])

    add("topic-14-2", "Tail call sum", "recursion", ["nums", "i", "acc"],
        "Return the sum using a tail-recursive helper: the accumulator is updated before the recursive call, and the recursive call's return is returned unchanged.",
        "Tail recursion stores the answer so far in acc. The last action of the call is the recursive call itself.",
        ["Start acc at 0.", "Call the helper with acc + nums[i].", "The base case returns acc."],
        "Accumulator comes first, then the call.",
        """
        def solve(nums):
            def walk(i, acc):
                if i == len(nums):
                    return acc
                return walk(i + 1, acc + nums[i])
            return walk(0, 0)
        """,
        ["solve([2, 4, 6])", "solve([])", "solve([5])"],
        expect=[12, 0, 5])

    add("topic-14-3", "All subsets", "recursion", ["path", "out", "i"],
        "Return every subset, including the empty one. Include the item before skipping it.",
        "Each call stores a choice in path. Two branches leave memory: one with the item appended, one after it is popped.",
        ["At the end, save a copy of path.", "Try including nums[i].", "Then try skipping it."],
        "Include, recurse, pop, skip.",
        """
        def solve(nums):
            out = []
            path = []

            def walk(i):
                if i == len(nums):
                    out.append(path[:])
                    return
                path.append(nums[i])
                walk(i + 1)
                path.pop()
                walk(i + 1)

            walk(0)
            return out
        """,
        ["solve([1, 2])", "solve([])", "solve([7])"],
        expect=[[[1, 2], [1], [2], []], [[]], [[7], []]])

    add("topic-14-4", "All orders", "recursion", ["path", "used", "out"],
        "Return every permutation of items.",
        "A permutation stores the chosen order in path and a used flag per index. Backtracking clears the flag when the call returns.",
        ["If path is complete, save it.", "Try each unused item.", "Pop it and mark it unused."],
        "Backtrack with a used list.",
        """
        def solve(items):
            out = []
            path = []
            used = []
            i = 0
            while i < len(items):
                used.append(False)
                i = i + 1

            def walk():
                if len(path) == len(items):
                    out.append(path[:])
                    return
                j = 0
                while j < len(items):
                    if not used[j]:
                        used[j] = True
                        path.append(items[j])
                        walk()
                        path.pop()
                        used[j] = False
                    j = j + 1

            walk()
            return out
        """,
        ["solve([1, 2])", "solve([1])", "solve([])"],
        expect=[[[1, 2], [2, 1]], [[1]], [[]]])

    add("topic-14-5", "Combination sum", "recursion", ["path", "out", "remain"],
        "nums is sorted. You may reuse a number. Return every combination that sums to target, in the order the recursion finds them.",
        "The path stores the numbers chosen so far. remain is the sum still needed. Reuse is allowed by calling the same index again.",
        ["If remain is 0, save path.", "Skip a number larger than remain.", "Append nums[i] and continue from i."],
        "Reuse is allowed. nums is sorted.",
        """
        def solve(nums, target):
            out = []
            path = []

            def walk(start, remain):
                if remain == 0:
                    out.append(path[:])
                    return
                i = start
                while i < len(nums):
                    if nums[i] > remain:
                        return
                    path.append(nums[i])
                    walk(i, remain - nums[i])
                    path.pop()
                    i = i + 1

            walk(0, target)
            return out
        """,
        ["solve([2, 3, 6, 7], 7)", "solve([2], 1)", "solve([1], 2)"],
        expect=[[[2, 2, 3], [7]], [], [[1, 1]]])

    add("topic-14-6", "Four queens", "matrix", ["cols", "diag", "anti", "row"],
        "Return how many ways 4 queens can be placed on a 4x4 board so none share a row, column, or diagonal.",
        "The call stack's depth is the row. cols, diag, and anti remember the lines already attacked.",
        ["Try a column in this row.", "Skip it when the column or a diagonal is taken.", "Count a solution when every row is filled."],
        "Backtracking count for n = 4. The argument is ignored; always solve 4 queens.",
        """
        def solve(n):
            n = 4
            cols = []
            diag = []
            anti = []
            i = 0
            while i < n:
                cols.append(False)
                i = i + 1
            i = 0
            while i < 2 * n:
                diag.append(False)
                anti.append(False)
                i = i + 1
            count = [0]

            def walk(row):
                if row == n:
                    count[0] = count[0] + 1
                    return
                c = 0
                while c < n:
                    d = row - c + n
                    a = row + c
                    if not cols[c] and not diag[d] and not anti[a]:
                        cols[c] = True
                        diag[d] = True
                        anti[a] = True
                        walk(row + 1)
                        cols[c] = False
                        diag[d] = False
                        anti[a] = False
                    c = c + 1

            walk(0)
            return count[0]
        """,
        ["solve(4)", "solve(0)"],
        expect=[2, 2])

    add("topic-14-7", "Fill the grid", "matrix", ["board", "r", "c"],
        "board is 4x4 sudoku using 1..4, with 0 for empty. Return the solved board. Each row, column, and 2x2 box contains 1..4 once.",
        "The empty cell is the decision. Trying a digit writes it into that memory slot, and a failure erases it before the next digit.",
        ["Find the next 0.", "Try a digit that is legal.", "Erase it if the rest of the board cannot be solved."],
        "Backtracking sudoku on a 4x4 board.",
        """
        def solve(board):
            grid = []
            for row in board:
                grid.append(row[:])

            def ok(r, c, val):
                i = 0
                while i < 4:
                    if grid[r][i] == val or grid[i][c] == val:
                        return False
                    i = i + 1
                br = (r // 2) * 2
                bc = (c // 2) * 2
                i = 0
                while i < 2:
                    j = 0
                    while j < 2:
                        if grid[br + i][bc + j] == val:
                            return False
                        j = j + 1
                    i = i + 1
                return True

            def walk():
                r = 0
                while r < 4:
                    c = 0
                    while c < 4:
                        if grid[r][c] == 0:
                            val = 1
                            while val <= 4:
                                if ok(r, c, val):
                                    grid[r][c] = val
                                    if walk():
                                        return True
                                    grid[r][c] = 0
                                val = val + 1
                            return False
                        c = c + 1
                    r = r + 1
                return True

            walk()
            return grid
        """,
        ["solve([[1, 2, 0, 4], [3, 4, 0, 2], [0, 1, 4, 3], [4, 3, 2, 1]])", "solve([[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]])"],
        expect=[[[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]], [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]])

    add("topic-14-8", "Out of the maze", "matrix", ["maze", "path"],
        "1 is open, 0 is a wall. Start at the top-left and reach the bottom-right moving only right or down. Return one path of [row, col], or an empty list.",
        "The path list is the route stored so far. A cell is marked 0 while it is on the path so the search does not reuse it, then restored on the way back.",
        ["Append the current cell.", "If it is the exit, stop.", "Try right, then down."],
        "Right and down only.",
        """
        def solve(maze):
            rows = len(maze)
            cols = len(maze[0])
            path = []

            def walk(r, c):
                if r < 0 or c < 0 or r >= rows or c >= cols or maze[r][c] != 1:
                    return False
                path.append([r, c])
                maze[r][c] = 0
                if r == rows - 1 and c == cols - 1:
                    return True
                if walk(r, c + 1) or walk(r + 1, c):
                    return True
                path.pop()
                maze[r][c] = 1
                return False

            grid = []
            for row in maze:
                grid.append(row[:])
            # walk closes over maze, so copy into the name the function reads
            maze = grid
            if walk(0, 0):
                return path
            return []
        """,
        ["solve([[1, 0], [1, 1]])", "solve([[1, 0], [0, 1]])", "solve([[1]])"],
        expect=[[[0, 0], [1, 0], [1, 1]], [], [[0, 0]]])

    add("topic-14-9", "Bounded knapsack", "recursion", ["best", "i", "left"],
        "Each item may be taken once. Return the maximum value with weight at most cap. Stop a branch when the weight would go negative or no items remain. This bound is the prune.",
        "Branch and bound here is the weight bound: a choice that exceeds cap is not explored. best stores the best value of a finished branch.",
        ["Skip the item, or take it when it fits.", "At the end, compare the value with best.", "Return best."],
        "0/1 search with a weight prune.",
        """
        def solve(weights, values, cap):
            best = [0]

            def walk(i, left, total):
                if total > best[0]:
                    best[0] = total
                if i == len(weights) or left == 0:
                    return
                walk(i + 1, left, total)
                if weights[i] <= left:
                    walk(i + 1, left - weights[i], total + values[i])

            walk(0, cap, 0)
            return best[0]
        """,
        ["solve([1, 3, 4], [1, 4, 5], 4)", "solve([5], [9], 4)", "solve([], [], 3)"],
        expect=[5, 0, 0])

    add("topic-14-10", "Stop early", "recursion", ["nums", "target", "count"],
        "nums is sorted positive. Return how many subsets sum to target. If the running sum already exceeds target, do not try further items.",
        "Pruning throws away a branch whose stored sum is already too big. The counter only grows on an exact hit.",
        ["If the sum equals target, count 1.", "If the sum is larger or the list ends, stop.", "Include the item, then skip it."],
        "Count subsets. Prune when the sum is too big.",
        """
        def solve(nums, target):
            count = [0]

            def walk(i, total):
                if total == target:
                    count[0] = count[0] + 1
                    return
                if total > target or i == len(nums):
                    return
                walk(i + 1, total + nums[i])
                walk(i + 1, total)

            walk(0, 0)
            return count[0]
        """,
        ["solve([1, 2, 3], 3)", "solve([1, 2], 5)", "solve([], 0)"],
        expect=[2, 0, 1])

