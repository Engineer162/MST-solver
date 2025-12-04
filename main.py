import math

def prim_mst(graph):
    n = len(graph)
    visited = [False] * n
    visited[0] = True  # Start i node 0

    mst_edges = []
    total_weight = 0

    for _ in range(n - 1):
        min_weight = math.inf
        u = v = -1

        # Find den billigste kant fra MST til ny node
        for i in range(n):
            if visited[i]:
                for j in range(n):
                    if not visited[j] and graph[i][j] != 0:
                        if graph[i][j] < min_weight:
                            min_weight = graph[i][j]
                            u, v = i, j

        visited[v] = True
        mst_edges.append((u, v, min_weight))
        total_weight += min_weight

    return mst_edges, total_weight


if __name__ == "__main__":
    graph = [
        [0, 1, 0, 0, 0, 9],
        [1, 0, 9, 7, 0, 0],
        [0, 9, 0, 9, 7, 0],
        [0, 7, 9, 0, 8, 0],
        [0, 0, 7, 8, 0, 4],
        [9, 0, 0, 0, 4, 0]
    ]

    mst, weight = prim_mst(graph)

    print("Minimum Spanning Tree:")
    for u, v, w in mst:
        print(f"Kant {u} — {v} med vægt {w}")

    print("Samlet vægt:", weight)
