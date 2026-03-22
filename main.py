import math
import matplotlib.pyplot as plt
import networkx as nx

# ── CITY GRAPH ──
locations = [
    ("Restaurant", 0, 0),
    ("Hotel",      2, 3),
    ("College",    1, -3),
    ("Market",     5, 2),
    ("Hospital",   5, -1),
    ("Park",       7, 3),
    ("Home",       8, -2),
    ("Bakery",     4, 5),
    ("School",     9, 1),
    ("Station",    10, -2),
]

edges = [
    ("Restaurant", "Hotel",    3),
    ("Restaurant", "College",  7),
    ("Hotel",      "Market",   2),
    ("Hotel",      "Hospital", 5),
    ("Hotel",      "Bakery",   4),
    ("College",    "Market",   4),
    ("College",    "Park",     6),
    ("Market",     "Hospital", 1),
    ("Market",     "Park",     3),
    ("Market",     "Bakery",   3),
    ("Hospital",   "Park",     2),
    ("Hospital",   "Home",     4),
    ("Hospital",   "School",   3),
    ("Park",       "Bakery",   2),
    ("Park",       "School",   4),
    ("Home",       "School",   3),
    ("Home",       "Station",  2),
    ("School",     "Station",  3),
]

# ── BUILD GRAPH ──
def build_graph(locations, edges):
    graph = {loc[0]: {} for loc in locations}
    for a, b, w in edges:
        graph[a][b] = w
        graph[b][a] = w
    return graph

# ── DIJKSTRA ──
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    unvisited = list(graph.keys())

    while unvisited:
        # pick unvisited node with smallest distance
        current = min(unvisited, key=lambda node: dist[node])
        unvisited.remove(current)

        for neighbor, weight in graph[current].items():
            new_dist = dist[current] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    return dist, prev

# ── GET PATH ──
def get_path(prev, dest):
    path = []
    cur = dest
    while cur:
        path.insert(0, cur)
        cur = prev[cur]
    return path

# ── GREEDY NEAREST NEIGHBOUR ──
def delivery_route(graph, start, stops):
    unvisited = stops.copy()
    current = start
    route = [start]
    all_paths = []
    total = 0

    print("\n=========================================")
    print("   FOOD DELIVERY ROUTE OPTIMIZER")
    print("=========================================")
    print(f"Starting from : {start}")
    print(f"Total orders  : {len(stops)}")
    print("-----------------------------------------")

    while unvisited:
        dist, prev = dijkstra(graph, current)

        # find nearest unvisited stop
        nearest = min(unvisited, key=lambda s: dist[s])
        path = get_path(prev, nearest)

        total += dist[nearest]
        all_paths.append((current, nearest, dist[nearest], path))
        route.append(nearest)
        unvisited.remove(nearest)

        print(f"\nStop {len(route)-1} → {nearest}")
        print(f"  Path     : {' -> '.join(path)}")
        print(f"  Distance : {dist[nearest]} km")
        print(f"  Total    : {total} km")

        current = nearest

    print("\n=========================================")
    print("  Delivery Complete!")
    print(f"  Total Distance  : {total} km")
    print(f"  Orders Delivered: {len(stops)} / {len(stops)}")
    print("  Algorithm Used  : Dijkstra + Greedy")
    print("=========================================")

    return route, all_paths, total

# ── VISUALIZATION ──
def visualize(locations, edges, route, all_paths):
    G = nx.Graph()
    pos = {loc[0]: (loc[1], loc[2]) for loc in locations}

    for loc in locations:
        G.add_node(loc[0])
    for a, b, w in edges:
        G.add_edge(a, b, weight=w)

    # collect route edges
    route_edges = []
    for _, _, _, path in all_paths:
        for i in range(len(path) - 1):
            route_edges.append((path[i], path[i+1]))

    # node colors
    node_colors = []
    for loc in locations:
        if loc[0] == route[0]:
            node_colors.append('#ff6b35')   # restaurant = orange
        elif loc[0] in route[1:]:
            node_colors.append('#00c97a')   # delivery stop = green
        else:
            node_colors.append('#4a4a4a')   # other = gray

    plt.figure(figsize=(12, 7))
    plt.title("Food Delivery Route Optimizer — Dijkstra + Greedy",
              fontsize=14, fontweight='bold', pad=20)

    # draw all edges (gray)
    nx.draw_networkx_edges(G, pos,
        edge_color='#cccccc', width=1, alpha=0.5)

    # draw route edges (green highlighted)
    nx.draw_networkx_edges(G, pos,
        edgelist=route_edges,
        edge_color='#00c97a', width=3)

    # draw nodes
    nx.draw_networkx_nodes(G, pos,
        node_color=node_colors,
        node_size=800)

    # draw labels
    nx.draw_networkx_labels(G, pos,
        font_size=8, font_color='white', font_weight='bold')

    # draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos,
        edge_labels={k: f"{v}km" for k, v in edge_labels.items()},
        font_size=7, font_color='#555555')

    # route order numbers
    for i, stop in enumerate(route[1:], 1):
        x, y = pos[stop]
        plt.annotate(str(i), xy=(x, y),
            xytext=(x + 0.3, y + 0.3),
            fontsize=9, fontweight='bold', color='#00c97a')

    # legend
    from matplotlib.patches import Patch
    legend = [
        Patch(color='#ff6b35', label='Restaurant (start)'),
        Patch(color='#00c97a', label='Delivery stop'),
        Patch(color='#4a4a4a', label='Other location'),
    ]
    plt.legend(handles=legend, loc='upper left', fontsize=9)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

# ── SAFE INPUT ──
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# ── MAIN ──
def main():
    graph = build_graph(locations, edges)

    print("SMART FOOD DELIVERY ROUTE OPTIMIZER\n")
    print("Available locations:")
    for loc in locations:
        print(f"  - {loc[0]}")

    restaurant = input("\nEnter restaurant name: ").strip()
    if restaurant not in graph:
        print("Location not found.")
        return

    stops = []
    n = get_int("Enter number of delivery stops: ")
    for i in range(n):
        stop = input(f"Stop {i+1}: ").strip()
        if stop not in graph:
            print(f"'{stop}' not found. Skipping.")
        else:
            stops.append(stop)

    if not stops:
        print("No valid stops entered.")
        return

    route, all_paths, total = delivery_route(graph, restaurant, stops)
    visualize(locations, edges, route, all_paths)

if __name__ == "__main__":
    main()