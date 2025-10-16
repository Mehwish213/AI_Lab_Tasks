from collections import deque

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.heuristics = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.adjacency_list:
            self.adjacency_list[node1] = []
        self.adjacency_list[node1].append((node2, weight))

    def set_heuristic(self, node, value):
        self.heuristics[node] = value

    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])

    def h(self, n):
        return self.heuristics.get(n, 1)

    def a_star_algorithm(self, start_node, stop_node):
        open_list = set([start_node])
        closed_list = set([])
        g = {start_node: 0}
        parents = {start_node: start_node}

        while len(open_list) > 0:
            n = None
            for v in open_list:
                if n is None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n is None:
                print("Path does not exist!")
                return None

            if n == stop_node:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start_node)
                reconst_path.reverse()
                print("Path found:", reconst_path)
                return reconst_path

            for (m, weight) in self.get_neighbors(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print("Path does not exist!")
        return None

graph = Graph()

num_edges = int(input("Enter number of edges: "))
for _ in range(num_edges):
    node1 = input("From node: ")
    node2 = input("To node: ")
    weight = int(input(f"Enter weight from {node1} to {node2}: "))
    graph.add_edge(node1, node2, weight)

num_nodes = int(input("\nEnter number of nodes (for heuristic values): "))
for _ in range(num_nodes):
    node = input("Node name: ")
    h_val = int(input(f"Heuristic value for {node}: "))
    graph.set_heuristic(node, h_val)

start = input("\nEnter Start Node: ")
end = input("Enter End Node: ")

print("\n🔹 Adjacency List:", graph.adjacency_list)
print("🔹 Heuristics:", graph.heuristics)
graph.a_star_algorithm(start, end)
