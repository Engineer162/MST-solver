import math  # importerer matematikmodulet (bruges for math.inf)
import matplotlib.pyplot as plt  # bruges til visualisering
import networkx as nx  # bruges til at bygge og tegne grafen


# -------- Prim (finder MST) --------
def prim_mst(graph):
    """
    Finder Minimum Spanning Tree (MST) for en vægtet, sammenhængende graf
    repræsenteret som en adjacency-matrix (2D liste).
    Returnerer en liste af kanter i formen (u, v, vægt).
    Bemærk: Funktionen antager at vægt 0 betyder ingen kant.
    """
    n = len(graph)
    visited = [False] * n
    visited[0] = True  # start fra node 0

    mst_edges = []

    # gentag n-1 gange for at finde alle kanter i MST
    for _ in range(n - 1):
        min_w = math.inf
        u = v = -1

        # søg efter den mindste kant som forbinder en besøgt node til en ikke-besøgt node
        for i in range(n):
            if visited[i]:
                for j in range(n):
                    if not visited[j] and graph[i][j] != 0:
                        if graph[i][j] < min_w:
                            min_w = graph[i][j]
                            u, v = i, j

        # markér den nye node som besøgt og tilføj kanten til MST'en
        visited[v] = True
        mst_edges.append((u, v, min_w))

    return mst_edges


# -------- byg adjacency list af MST --------
def build_tree(mst_edges, n):
    """
    Bygger en adjacency-list repræsentation (ordbog) af MST'en.
    Hver nøgle er en node, værdien er en liste af (nbr, vægt)-tupler.
    Dette gør det nemt at traversere MST'en senere (f.eks. DFS).
    """
    tree = {i: [] for i in range(n)}
    for u, v, w in mst_edges:
        tree[u].append((v, w))
        tree[v].append((u, w))
    return tree


# -------- find vej i MST (DFS) --------
def find_path(tree, start, end):
    """
    Finder en vilkårlig sti fra start til end i MST'en ved hjælp af DFS.
    Returnerer en liste af kanter (u, v) i den rækkefølge de besøges på stien.
    Stien gemmes som orienterede kant-par for nem visualisering/udskrivning.
    """
    visited = set()
    path = []

    def dfs(u):
        if u == end:
            return True
        visited.add(u)

        for v, _ in tree[u]:
            if v not in visited:
                path.append((u, v))  # tilføj kant på stiens sti
                if dfs(v):
                    return True
                path.pop()  # backtrack hvis denne vej ikke fører til mål
        return False

    dfs(start)
    return path


# -------- Visualisering --------
def draw(graph, mst_edges, path, start, end):
    """
    Tegner hele grafen, markerer MST'en og fremhæver den fundne sti.
    - Hele grafen: lysegrå kanter
    - MST: tykkere grå kanter
    - Fundet sti i MST: rød, tykkere kanter
    Start- og slutnoder fremhæves med farver.
    """
    G = nx.Graph()
    n = len(graph)

    # tilføj noder
    for i in range(n):
        G.add_node(i)

    # tilføj kanter fra adjacency-matrix
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] != 0:
                G.add_edge(i, j, weight=graph[i][j])

    pos = nx.circular_layout(G)  # layout til placering af noder i cirkel

    plt.figure(figsize=(8, 8))

    # Alle kanter (lys grå)
    nx.draw(G, pos, node_color="lightblue", node_size=800,
            edge_color="lightgray", with_labels=True)

    # MST (tykkere grå kanter)
    nx.draw_networkx_edges(
        G, pos,
        edgelist=[(u, v) for u, v, _ in mst_edges],
        width=3
    )

    # Mindst-vægt-vej i MST (rød, fremhævet)
    nx.draw_networkx_edges(
        G, pos,
        edgelist=path,
        edge_color="red",
        width=4
    )

    # Kantvægte som labels
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Fremhæv start- og slutnoder
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color="green", node_size=900)
    nx.draw_networkx_nodes(G, pos, nodelist=[end], node_color="orange", node_size=900)

    plt.title("Grå = Minimum Spanning Tree | Rød = Mindst-vægt-vej i MST")
    plt.axis("off")
    plt.show()


# -------- MAIN --------
if __name__ == "__main__":
    # Eksempel: adjacency-matrix for en vægtet, urettet graf
    # 0 betyder ingen kant mellem to noder
    graph = [
        [0, 1, 0, 7, 0, 0],
        [1, 0, 8, 1, 0, 0],
        [0, 8, 0, 4, 4, 0],
        [7, 1, 4, 0, 5, 0],
        [0, 0, 4, 5, 0, 4],
        [0, 0, 0, 0, 4, 0]
    ]

    start = 0  # startnode for at finde sti i MST
    end = 5    # slutnode

    mst = prim_mst(graph)  # beregn MST vha. Prim
    tree = build_tree(mst, len(graph))  # lav adjacency-list for MST
    path = find_path(tree, start, end)  # find sti fra start til end i MST

    # Udskriv den fundne sti og dens samlede vægt
    print("Mindst-vægt-vej i MST:")
    total = 0
    for u, v in path:
        w = graph[u][v]
        total += w
        print(f"{u} → {v} (vægt {w})")

    print("Samlet vægt:", total)

    draw(graph, mst, path, start, end)
