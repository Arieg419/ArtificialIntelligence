#
# class Graph:  # took it from search.py and made changes
#     """A graph connects nodes (verticies) by edges (links).
#     The constructor call is something like:
#         g = Graph({'A': ({A,C},["driver"]),....)
#     this makes a graph with 3 nodes, A, B, and C, with an edge of from
#     A to B,  and an edge of from A to C.  At the node A there is a driver.
#     You can also do: g = Graph({'A': {A,C}, directed=False)
#     This makes an undirected graph, so inverse links are also added.
#     You can use g.nodes() to get a list of nodes.
#     g.get('A') to get a dict of links out of A.
#     nodes can be any hashable object."""
#
#     def __init__(self, dict=None, directed=True):
#         self.dict = dict or {}
#         self.directed = directed
#         if not directed: self.make_undirected()
#
#     def make_undirected(self):
#         "Make a digraph into an undirected graph by adding symmetric edges."
#         for a in self.dict.keys():
#             for b in self.dict[a][0]:
#                 self.connect(b, a)
#
#     def connect(self, A, B):
#         "Add a link from A to B of given distance, in one direction only."
#         self.dict[A][0].add(B)
#
#     def get_neighbours(self, a):
#         # get(a) returns a set of the neighbours
#         return self.dict[a][0]
#
#     def nodes(self):
#         "Return a list of nodes in the graph."
#         return self.dict.keys()
#
#     def driver(self, a):
#         return "driver" in self.dict[a][1]
#
#     def truck(self, a):
#         return "truck" in self.dict[a][1]
#
#     def package(self, a):
#         return "package" in self.dict[a][1]
#
# # -------------creating a graph represented in adjacency list form----------
# drivers_location = [city[1] for city in node.state[6][0]]
# trucks_location = [city[1] for city in node.state[6][1]]
# packages_location = [city[1] for city in node.state[6][2]]
# city_dict = {}
# for truck, city in node.state[6][1]:
#     if city not in city_dict.keys():
#         city_dict[city] = []
#         city_dict[city].append(truck)
#     else:
#         city_dict[city].append(truck)
# dict_graph = {}
# for package, city in node.state[6][2]:
#     if city not in city_dict.keys():
#         city_dict[city] = []
#         city_dict[city].append(package)
#     else:
#         city_dict[city].append(package)
# for city in node.state[3]:
#     dict_graph[city] = (set(), [])
#     if city in drivers_location:
#         dict_graph[city][1].append("driver")
#     if city in trucks_location:
#         dict_graph[city][1].append("truck")
#     if city in packages_location:
#         dict_graph[city][1].append("package")
# for road in node.state[4]:
#     dict_graph[str(road[0])][0].add(road[1])
# g = Graph(dict_graph, directed=False)
#
# # BFS for each goal------------------------------need to adjust fot goals which are drivers inside truck + check the curent state
# def BFS_distance(root):
#     dist_OR_visited, queue = {}, collections.deque([root])
#     dist_OR_visited[root] = 0
#     distance = 0
#     nodes_calculated = 0
#     while queue:
#         vertex = queue.popleft()
#         for neighbour in g.get_neighbours(vertex):
#             if neighbour not in dist_OR_visited:
#                 dist_OR_visited[neighbour] = dist_OR_visited[vertex] + 1  # coloring the vertex in Black
#                 queue.append(neighbour)
#                 if g.driver(neighbour) and g.truck(neighbour):
#                     return dist_OR_visited[neighbour]
#                 elif g.driver(neighbour) or g.truck(neighbour):
#                     nodes_calculated += 1
#                     distance += dist_OR_visited[neighbour]
#                     if nodes_calculated == 2:
#                         return distance
#     return infinity
#                         # -------------------------------------add all combinations of if to calculate the distance
#
# # ---------------------------do we need to check if the current state is goal?
# goals_distance = 0
# # check if it's goal
# for goal in self.goal:
#     goals_distance += BFS_distance(goal[1])
# return goals_distance