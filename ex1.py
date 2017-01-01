import search
import random
import math
import collections
from utils import infinity
from copy import deepcopy

ids = ["111111111", "111111111"]
builtCityDict = False
keysForCities = ["Drivers", "Trucks", "Packages"]
truckIdx = 1
locationIdx = 3
linksIdx = 4
pathsIdx = 5
startingPositionsIdx = 6
goalIdx = 7


# inherits from search.Problem
class DriverlogProblem(search.Problem):
    def __init__(self, initial, goal):
        self.goal = goal
        self.origState = ""
        self.cityDictionary = {}
        self.nextStates = []
        self.newActions = []
        search.Problem.__init__(self, initial, goal)
        self.stateRep = ["Drivers: ", "Trucks", "Packages: ", "Locations: ", "Links: ", "Path: ", "Starting Position: ",
                         "Goal: "]

    def printState(self, state):
        print "********&&&&&&&&&&& PrintState Function ********&&&&&&&&&&& "
        for i, item in enumerate(state):
            print self.stateRep[i], item, "\n"
        print "********&&&&&&&&&&& PrintState Function End ********&&&&&&&&&&& "

    def printCitiesInDict(self, state, cityDictionary):
        # Printing all Cities
        print "*************************** LocationDict ***************************"
        for idx, val in enumerate(cityDictionary):
            if val in self.origState[1]:
                continue
            print "********************* Location ", val, "*********************\n"
            print "Drivers: ", cityDictionary[val]["Drivers"], "\n"
            print "Trucks: ", cityDictionary[val]["Trucks"], "\n"
            print "Packages: ", cityDictionary[val]["Packages"], "\n"
            print "Links: ", cityDictionary[val]["Links"], "\n"
            print "Paths: ", cityDictionary[val]["Paths"], "\n"
            print "********************* Location ", val, " End *********************\n"
        print "*************************** LocationDict End ***********************"

        # Printing all Trucks
    def printingTrucksInDict(self, state, cityDictionary):
        for idx, val in enumerate(cityDictionary):
            if val in self.origState[1]:
                print "********************* Location ", val, "*********************\n"
                print "Drivers: ", cityDictionary[val]["Drivers"], "\n"
                print "Packages: ", cityDictionary[val]["Packages"], "\n"
                print "Location: ", cityDictionary[val]["Location"], "\n"
                print "********************* Location ", val, " End *********************\n"


    def addCitiesToDict(self, state):
        for idx in range(len(state[locationIdx])):
            self.cityDictionary[state[locationIdx][idx]] = {
                "Drivers": [],
                "Trucks": [],
                "Packages": [],
                "Links": [],
                "Paths": []
            }

        for idx in range(len(state[truckIdx])):
            self.cityDictionary[state[truckIdx][idx]] = {
                "Drivers": [],
                "Packages": [],
                "Location": []
            }

    def mapStartingPosToCityDict(self, state):
        # Adding Drivers, Trucks and Packages to CityDictionary
        for key, item in enumerate(state[startingPositionsIdx]):
            for i, (identifier, city) in enumerate(state[startingPositionsIdx][key]):
                self.cityDictionary[city][keysForCities[key]].append(identifier)

        # Adding Locations to Trucks
        for idx, val in enumerate(self.cityDictionary):
            if val in self.origState[1]:
                continue
            for truck in self.cityDictionary[val]["Trucks"]:
                self.cityDictionary[truck]["Location"] = val


        # Adding Links to CityDictionary
        for key, item in enumerate(state[linksIdx]):
            origin, destination = state[linksIdx][key]
            if destination not in self.cityDictionary[origin]["Links"]:
                self.cityDictionary[origin]["Links"].append(destination)
            if origin not in self.cityDictionary[destination]["Links"]:
                self.cityDictionary[destination]["Links"].append(origin)

        # Adding Paths to CityDictionary
        for key, item in enumerate(state[pathsIdx]):
            origin, destination = state[pathsIdx][key]
            if destination not in self.cityDictionary[origin]["Links"]:
                self.cityDictionary[origin]["Paths"].append(destination)
            if origin not in self.cityDictionary[destination]["Links"]:
                self.cityDictionary[destination]["Paths"].append(origin)

    def compute_load_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[2] = list(deepcopy(newState[2]))  # problem
        for idx, val in enumerate(cityDictionary):
            if val in self.origState[1]: # check that we are not iterating over a truck
                continue
            if len(cityDictionary[val]["Trucks"]) == 0 or len(cityDictionary[val]["Packages"]) == 0:
                continue
            for package in state[2]:  # ('a', '1') or ('a', 'mazda')
                if package[1] in self.origState[1]:
                    continue
                if package[0] in cityDictionary[val]["Packages"]:
                    for truck in cityDictionary[val]["Trucks"]:
                        if ("load_truck", package[0], truck) in self.newActions:
                            continue
                        newState[2].remove(package)
                        newState[2].append((package[0], truck))
                        newState[2] = tuple(deepcopy(newState[2]))
                        newState = tuple(deepcopy(newState))
                        self.newActions.append(("load_truck", package[0], truck))
                        yield ("load_truck", package[0], truck), (newState)  # act, state
                        newState = list(newState)
                        newState[2] = list(newState[2])
                        newState[2].remove((package[0], truck))
                        newState[2].append(package)


    def compute_unload_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[2] = list(deepcopy(newState[2])) # package car list
        for idx, truck in enumerate(cityDictionary):
            if truck not in self.origState[1]: # only for trucks
                continue
            for package in state[2]: # state[2] is packages
                if package[1] not in self.origState[1]: # only want to unload package from trucks
                    continue
                if truck == package[1]: # finding current truck
                    if ("unload_truck", package[0], truck) in self.newActions:
                        continue
                    truckLocation = self.cityDictionary[truck]["Location"]
                    self.newActions.append(("unload_truck", package[0], truck))
                    newState[2].remove(package)
                    newState[2].append((package[0], truckLocation))
                    newState[2] = tuple(deepcopy(newState[2]))
                    newState = tuple(deepcopy(newState))
                    yield ("unload_truck", package[0], truck), (newState)  # act, state
                    newState = list(newState)
                    newState[2] = list(newState[2])
                    newState[2].append(package)
                    newState[2].remove((package[0], truckLocation))

    # TODO what if a driver is already on a truck?!?!
    def compute_board_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[0] = list(deepcopy(newState[0]))
        for idx, val in enumerate(cityDictionary):
            if val in self.origState[1]: # only run for cities and not trucks
                continue
            if len(cityDictionary[val]["Trucks"]) == 0 or len(cityDictionary[val]["Drivers"]) == 0:
                continue
            for driver in state[0]:
                if driver[0] in cityDictionary[val]["Drivers"]:
                    for truck in cityDictionary[val]["Trucks"]:
                        if ("board_truck", driver[0], truck) in self.newActions:
                            continue
                        if len(cityDictionary[truck]["Drivers"]) > 0: # there is already a driver on truck
                            continue
                        self.newActions.append(("board_truck", driver[0], truck))
                        newState[0].remove(driver)
                        newState[0].append((driver[0], truck))
                        newState[0] = tuple(deepcopy(newState[0]))
                        newState = tuple(deepcopy(newState))
                        yield ("board_truck", driver[0], truck), (newState)
                        newState = list(newState)
                        newState[0] = list(newState[0])
                        newState[0].append(driver)
                        newState[0].remove((driver[0], truck))

    # TODO optimization: cache all starting positions into global variables
    def compute_disembark_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[0] = list(deepcopy(newState[0]))
        for idx, truck in enumerate(cityDictionary):
            if truck not in self.origState[1]:  # only run for trucks
                continue
            if len(cityDictionary[truck]["Drivers"]) == 0:
                continue
            for driver in state[0]:
                if driver[0] in cityDictionary[truck]["Drivers"]:
                    if ("disembark_truck", driver[0], truck) in self.newActions:
                        continue
                    truckLocation = cityDictionary[truck]["Location"]
                    self.newActions.append(("disembark_truck", driver[0], truck))
                    newState[0].remove(driver)
                    newState[0].append((driver[0], truckLocation))
                    newState[0] = tuple(deepcopy(newState[0]))
                    newState = tuple(deepcopy(newState))
                    yield ("disembark_truck", driver[0], truck), (newState)
                    newState = list(newState)
                    newState[0] = list(newState[0])
                    newState[0].append(driver)
                    newState[0].remove((driver[0], truckLocation))



    def compute_drive_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[1] = list(deepcopy(newState[1]))
        for idx, truck in enumerate(cityDictionary):
            if truck not in self.origState[1]: # only on trucks
                continue
            if len(cityDictionary[truck]["Drivers"]) == 0: # no drivers on trucks
                continue
            for driver in state[0]: # driver is (driver, truck)
                if driver[1] not in self.origState[1]:
                    continue
                if driver[0] in cityDictionary[truck]["Drivers"]:
                    truckLocation = cityDictionary[truck]["Location"]
                    for link in cityDictionary[truckLocation]["Links"]:
                        isThisIt = ("drive_truck", truck, truckLocation, link)
                        if isThisIt in self.newActions:
                            continue
                        self.newActions.append(("drive_truck", truck, truckLocation, link))
                        newState[1].remove((truck, truckLocation))
                        newState[1].append((truck, link))
                        newState[1] = tuple(deepcopy(newState[1]))
                        newState = tuple(deepcopy(newState))
                        yield (("drive_truck", truck, truckLocation, link), (newState))
                        newState = list(newState)
                        newState[1] = list(newState[1])
                        newState[1].append((truck, truckLocation))
                        newState[1].remove((truck, link))


    def compute_walk_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[0] = list(deepcopy(newState[0]))  # list of driver positions
        for idx, city in enumerate(cityDictionary):
            if city in self.origState[1]:  # only on cities
                continue
            if len(cityDictionary[city]["Drivers"]) == 0:
                continue
            for driver in state[0]:  # driver is (driver, city)
                if driver[0] in cityDictionary[city]["Drivers"]:
                    for path in cityDictionary[city]["Paths"]:
                        #print "************** PATH TIME *****************", path
                        if ("walk ", driver[0], city, path) in self.newActions:
                            continue
                        self.newActions.append(("walk", driver[0], city, path))
                        newState[0].remove(driver)
                        newState[0].append((driver[0], path))
                        newState[0] = tuple(deepcopy(newState[0]))
                        newState = tuple(deepcopy(newState))
                        yield (("walk", driver[0], city, path), (newState))
                        newState = list(newState)
                        newState[0] = list(newState[0])
                        newState[0].append(driver)
                        newState[0].remove((driver[0], path))

    def buildRetValue(self, state, newState):
        # get state, turn to list
        tmpState = list(deepcopy(state))
        tmpState[6] = newState
        tmpState = tuple(tmpState)
        return tmpState


    def successor(self, state):
        self.cityDictionary = {}
        self.origState = state
        self.addCitiesToDict(state)
        self.mapStartingPosToCityDict(state)
        self.newActions = []
        self.nextStates = []
        currState = state[6]
        # print "self goal is ", self.goal

        for act, newState in self.compute_load_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        for act, newState in self.compute_unload_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        for act, newState in self.compute_board_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        for act, newState in self.compute_disembark_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        for act, newState in self.compute_drive_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        for act, newState in self.compute_walk_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        # print "*************************** NewState before yield *******************************"
        # for item in self.nextStates:
        #     print item, "\n"
        # print "*************************** END NewState before yield *******************************"

        #print self.nextStates
        return self.nextStates
        #print len(self.nextStates)
        #return self.nextStates





            # for item in self.compute_walk_moves(state, cityDictionary):
            #     # TODO do i need to return the whole world information, or only new positions?
            #     self.nextStates.append(item)


            # #return self.nextStates
            # for item in self.nextStates:
            #     print item, "\n"

    def goal_test(self, state):
        if state[6][2] == self.goal:
            return True
        return False

    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate
        Must return an integer"""

        class Graph:  # took it from search.py and made changes
            """A graph connects nodes (verticies) by edges (links).
            The constructor call is something like:
                g = Graph({'A': ({A,C},["driver"]),....)
            this makes a graph with 3 nodes, A, B, and C, with an edge of from
            A to B,  and an edge of from A to C.  At the node A there is a driver.
            You can also do: g = Graph({'A': {A,C}, directed=False)
            This makes an undirected graph, so inverse links are also added.
            You can use g.nodes() to get a list of nodes.
            g.get('A') to get a dict of links out of A.
            nodes can be any hashable object."""

            def __init__(self, dict=None, directed=True):
                self.dict = dict or {}
                self.directed = directed
                if not directed: self.make_undirected()

            def make_undirected(self):
                "Make a digraph into an undirected graph by adding symmetric edges."
                for a in self.dict.keys():
                    for b in self.dict[a][0]:
                        self.connect(b, a)

            def connect(self, A, B):
                "Add a link from A to B of given distance, in one direction only."
                self.dict[A][0].add(B)

            def get_neighbours(self, a):
                # get(a) returns a set of the neighbours
                return self.dict[a][0]

            def nodes(self):
                "Return a list of nodes in the graph."
                return self.dict.keys()

            def driver(self, a):
                return "driver" in self.dict[a][1]

            def truck(self, a):
                return "truck" in self.dict[a][1]

            def package(self, a):
                return "package" in self.dict[a][1]

        # -------------creating a graph represented in adjacency list form----------
        drivers_location = [city[1] for city in node.state[6][0]]
        trucks_location = [city[1] for city in node.state[6][1]]
        packages_location = [city[1] for city in node.state[6][2]]
        city_dict = {}
        for truck, city in node.state[6][1]:
            if city not in city_dict.keys():
                city_dict[city] = []
                city_dict[city].append(truck)
            else:
                city_dict[city].append(truck)
        dict_graph = {}
        for package, city in node.state[6][2]:
            if city not in city_dict.keys():
                city_dict[city] = []
                city_dict[city].append(package)
            else:
                city_dict[city].append(package)
        for city in node.state[3]:
            dict_graph[city] = (set(), [])
            if city in drivers_location:
                dict_graph[city][1].append("driver")
            if city in trucks_location:
                dict_graph[city][1].append("truck")
            if city in packages_location:
                dict_graph[city][1].append("package")
        for road in node.state[4]:
            dict_graph[str(road[0])][0].add(road[1])
        g = Graph(dict_graph, directed=False)

        # BFS for each goal------------------------------need to adjust fot goals which are drivers inside truck + check the curent state
        def BFS_distance(root):
            dist_OR_visited, queue = {}, collections.deque([root])
            dist_OR_visited[root] = 0
            distance = 0
            nodes_calculated = 0
            while queue:
                vertex = queue.popleft()
                for neighbour in g.get_neighbours(vertex):
                    if neighbour not in dist_OR_visited:
                        dist_OR_visited[neighbour] = dist_OR_visited[vertex] + 1  # coloring the vertex in Black
                        queue.append(neighbour)
                        if g.driver(neighbour) and g.truck(neighbour):
                            return dist_OR_visited[neighbour]
                        elif g.driver(neighbour) or g.truck(neighbour):
                            nodes_calculated += 1
                            distance += dist_OR_visited[neighbour]
                            if nodes_calculated == 2:
                                return distance
            return infinity
                                # -------------------------------------add all combinations of if to calculate the distance

        # ---------------------------do we need to check if the current state is goal?
        goals_distance = 0
        # check if it's goal
        for goal in self.goal:
            goals_distance += BFS_distance(goal[1])
        return goals_distance



def create_driverlog_problem(problem):
    goal = problem[-1]
    """ Create a driverlog problem, based on the description.
    problem -- nested tuple as it was described in the description pdf file """

    return DriverlogProblem(problem, goal)
