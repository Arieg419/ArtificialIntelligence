import search
import random
import math
import collections
from utils import infinity
from copy import deepcopy

ids = ["111111111", "111111111"]
builtCityDict = False
keysForCities = ["Drivers", "Trucks", "Packages"]

# Indexes for original state data
truckIdx = 1
packageIdx = 2
locationIdx = 3
linksIdx = 4
pathsIdx = 5
startingPositionsIdx = 6
goalIdx = 7

# Indexes for curr state data
currDriverIdx = 0
currTruckIdx = 1
currPackIdx = 2

def bfs(startNode, cities):
    queue = []
    startNode.visited = True
    queue.append(startNode)
    distDict = {}
    for city in cities:
        distDict[city] = float("inf")
    while queue:
        actualNode = queue.pop()
        for n in actualNode.adjacenciesList:
            if not n.visited:
                n.visited = True
                queue.append(n)
                distDict[n.name] = distDict[actualNode.name] + 1
            else:
                if distDict[n.name] > distDict[actualNode.name] + 1:
                    distDict[n.name] = distDict[actualNode.name] + 1
    return distDict

class BFSnode:
    def __init__(self, name):
        self.name = name
        self.adjacenciesList = []
        self.visited = False

    def printAdjacencies(self):
        for neighbor in self.adjacenciesList:
            print neighbor.name

class Graph:
    def __init__(self, typeOfTransport):
        self.nodesList = []
        self.typeOfTransport = typeOfTransport

    def createGraph(self, node):
        for city in node[locationIdx]:
            currNode = BFSnode(city)
            for link in node[self.typeOfTransport]: # link is (origin, destination)
                if link[0] == city:
                    currNode.adjacenciesList.append(BFSnode(link[1]))
                if link[1] == city:
                    currNode.adjacenciesList.append(BFSnode(link[0]))
            self.nodesList.append(currNode)

    def printGraph(self):
        print "********* Printing Graph *********\n"
        for node in self.nodesList:
            print "Node: ", node.name, "\nNeighbors: "
            node.printAdjacencies()
            print "\n"
        print "********* End of Printing Graph *********\n"



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
            for (identifier, loc) in item:
                self.cityDictionary[loc][keysForCities[key]].append(identifier)

        # Adding Locations to Trucks
        for idx, val in enumerate(self.cityDictionary):
            if val in self.origState[truckIdx]:
                continue
            for truck in self.cityDictionary[val]["Trucks"]:
                self.cityDictionary[truck]["Location"] = val

        # Adding Links to CityDictionary, Links are bi-directional
        for key, item in enumerate(state[linksIdx]):
            origin, destination = state[linksIdx][key]
            if destination not in self.cityDictionary[origin]["Links"]:
                self.cityDictionary[origin]["Links"].append(destination)
            if origin not in self.cityDictionary[destination]["Links"]:
                self.cityDictionary[destination]["Links"].append(origin)

        # Adding Paths to CityDictionary, Paths are bi-directional
        for key, item in enumerate(state[pathsIdx]):
            origin, destination = state[pathsIdx][key]
            if destination not in self.cityDictionary[origin]["Paths"]:
                self.cityDictionary[origin]["Paths"].append(destination)
            if origin not in self.cityDictionary[destination]["Paths"]:
                self.cityDictionary[destination]["Paths"].append(origin)

    def compute_load_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[currPackIdx] = list(deepcopy(newState[currPackIdx]))
        for package, loc in state[currPackIdx]:
            if loc in self.origState[locationIdx]:
                trucks = cityDictionary[loc]["Trucks"]
                for truck in trucks:
                    if ("load_truck", package, truck) in self.newActions:
                        continue
                    newState[currPackIdx].remove((package, loc))
                    newState[currPackIdx].append((package, truck))
                    newState[currPackIdx] = tuple(deepcopy(newState[currPackIdx]))
                    newState = tuple(deepcopy(newState))
                    self.newActions.append(("load_truck", package, truck))
                    yield ("load_truck", package, truck), (newState)  # act, state
                    newState = list(newState)
                    newState[currPackIdx] = list(newState[currPackIdx])
                    newState[currPackIdx].remove((package, truck))
                    newState[currPackIdx].append((package, loc))

    def compute_unload_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[currPackIdx] = list(deepcopy(newState[currPackIdx]))  # package car list
        for package, loc in state[currPackIdx]:
            if loc in self.origState[truckIdx]:
                city = cityDictionary[loc]["Location"]
                if ("unload_truck", package, loc) in self.newActions:
                    continue
                self.newActions.append(("unload_truck", package[0], loc))
                newState[currPackIdx].remove((package, loc))
                newState[currPackIdx].append((package, city))
                newState[currPackIdx] = tuple(deepcopy(newState[currPackIdx]))
                newState = tuple(deepcopy(newState))
                yield ("unload_truck", package, loc), (newState)  # act, state
                newState = list(newState)
                newState[currPackIdx] = list(newState[currPackIdx])
                newState[currPackIdx].append((package, loc))
                newState[currPackIdx].remove((package, city))

    def compute_board_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[currDriverIdx] = list(deepcopy(newState[currDriverIdx]))
        for driver, loc in state[currDriverIdx]:
            if loc in self.origState[locationIdx]:
                trucks = cityDictionary[loc]["Trucks"]
                for truck in trucks:
                    if ("board_truck", driver, truck) in self.newActions:
                        continue
                    if len(cityDictionary[truck]["Drivers"]) > 0:  # there is already a driver on truck
                        continue
                    self.newActions.append(("board_truck", driver, truck))
                    newState[currDriverIdx].remove((driver, loc))
                    newState[currDriverIdx].append((driver, truck))
                    newState[currDriverIdx] = tuple(deepcopy(newState[currDriverIdx]))
                    newState = tuple(deepcopy(newState))
                    yield ("board_truck", driver, truck), (newState)
                    newState = list(newState)
                    newState[currDriverIdx] = list(newState[currDriverIdx])
                    newState[currDriverIdx].append((driver, loc))
                    newState[currDriverIdx].remove((driver, truck))

    def compute_disembark_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[currDriverIdx] = list(deepcopy(newState[currDriverIdx]))
        for driver, loc in state[currDriverIdx]:
            if loc in self.origState[truckIdx]:
                city = cityDictionary[loc]["Location"]
                if ("disembark_truck", driver, loc) in self.newActions:
                    continue
                self.newActions.append(("disembark_truck", driver, loc))
                newState[currDriverIdx].remove((driver, loc))
                newState[currDriverIdx].append((driver, city))
                newState[currDriverIdx] = tuple(deepcopy(newState[currDriverIdx]))
                newState = tuple(deepcopy(newState))
                yield ("disembark_truck", driver, loc), (newState)
                newState = list(newState)
                newState[currDriverIdx] = list(newState[currDriverIdx])
                newState[currDriverIdx].append((driver, loc))
                newState[currDriverIdx].remove((driver, city))

    def compute_drive_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[currTruckIdx] = list(deepcopy(newState[1]))
        for truck, city in state[currTruckIdx]:
            for link in cityDictionary[city]["Links"]:
                if ("drive_truck", truck, city, link) in self.newActions:
                    continue
                self.newActions.append(("drive_truck", truck, city, link))
                newState[currTruckIdx].remove((truck, city))
                newState[currTruckIdx].append((truck, link))
                newState[currTruckIdx] = tuple(deepcopy(newState[currTruckIdx]))
                newState = tuple(deepcopy(newState))
                yield ("drive_truck", truck, city, link), (newState)
                newState = list(newState)
                newState[currTruckIdx] = list(newState[currTruckIdx])
                newState[currTruckIdx].append((truck, city))
                newState[currTruckIdx].remove((truck, link))

    def compute_walk_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[currDriverIdx] = list(deepcopy(newState[currDriverIdx]))  # list of driver positions
        for driver in state[currDriverIdx]:  # driver is (driver, city) or (driver, truck)
            if driver[1] not in self.origState[locationIdx]:
                continue
            for path in cityDictionary[driver[1]]["Paths"]:
                if ("walk ", driver[0], driver[1], path) in self.newActions:
                    continue
                self.newActions.append(("walk", driver[0], driver[1], path))
                newState[currDriverIdx].remove(driver)
                newState[currDriverIdx].append((driver[0], path))
                newState[currDriverIdx] = tuple(deepcopy(newState[0]))
                newState = tuple(deepcopy(newState))
                yield ("walk", driver[0], driver[1], path), (newState)
                newState = list(newState)
                newState[currDriverIdx] = list(newState[currDriverIdx])
                newState[currDriverIdx].append(driver)
                newState[currDriverIdx].remove((driver[0], path))

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

        #print "1"
        for act, newState in self.compute_load_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        #print "2"
        for act, newState in self.compute_unload_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        #print "3"
        for act, newState in self.compute_board_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        #print "4"
        for act, newState in self.compute_disembark_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        #print "5"
        for act, newState in self.compute_drive_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        #print "6"
        # print currState
        for act, newState in self.compute_walk_moves(currState, self.cityDictionary):
            # print act, "\n", state, "\n", newState
            self.nextStates.append((act, self.buildRetValue(state, newState)))

        # print "*************************** NewState before yield *******************************"
        # for item in self.nextStates:
        #     print item, "\n"
        # print "*************************** END NewState before yield *******************************"

        # print self.nextStates
        # if len(self.nextStates) > 0:
        #     print "Not empty"
        # else:
        #     print "Empty"
        return self.nextStates
        # print len(self.nextStates)
        # return self.nextStates





        # for item in self.compute_walk_moves(state, cityDictionary):
        #     # TODO do i need to return the whole world information, or only new positions?
        #     self.nextStates.append(item)


        # #return self.nextStates
        # for item in self.nextStates:
        #     print item, "\n"

    def goal_test(self, state):
        for tupel in self.goal:
            s = state[startingPositionsIdx]
            if tupel not in s[currDriverIdx] and tupel not in s[currTruckIdx] and tupel not in s[currPackIdx]:
                return False
        return True

    def driver_h(self, node, linkgraph, pathgraph, penalty):
        for driver, loc in node.state[startingPositionsIdx][currDriverIdx]: # (driver, location) or (driver,truck)
            importantDriver = 0
            for couple in self.goal: # does this driver even appear in the goal
                if couple[0] == driver:
                    importantDriver = 1
                    driverGoalLoc = couple[1]
                    break
            if importantDriver == 0: # if the driver doesn't appear in the goal, skip him
                continue
            if (driver, loc) not in self.goal:
                if loc in node.state[locationIdx]: # if the driver is currently in a city
                    # do bfs on pathGraph to find distance between loc and driverGoalLoc
                    for path in pathgraph.nodesList:
                        if path.name == driverGoalLoc:
                            distPathDict = bfs(path, node.state[locationIdx])
                            penalty = penalty + distPathDict[loc]
                            break
                    # bfs on linkGraph to find distance between loc and driverGoalLoc + add penalty for getting on truck
                    for link in linkgraph.nodesList:
                        if link.name == driverGoalLoc:
                            distLinkDict = bfs(link, node.state[locationIdx])
                            penalty = penalty + distLinkDict[loc] + 10
                            break
                else: # driver is currently in truck
                    # find what city the truck is in
                    for truck, city in node.state[startingPositionsIdx][currTruckIdx]:
                        if truck == loc:
                            # do bfs on pathGraph to find distance between city and driverGoalLoc + penalty
                            for path in pathgraph.nodesList:
                                if path.name == driverGoalLoc:
                                    distPathDict = bfs(path, node.state[locationIdx])
                                    penalty = penalty + distPathDict[city] + 5
                                    break
                            # bfs on linkGraph to find distance between city and driverGoalLoc
                            for link in linkgraph.nodesList:
                                if link.name == driverGoalLoc:
                                    distLinkDict = bfs(link, node.state[locationIdx])
                                    penalty = penalty + distLinkDict[city]
                                    break
        return penalty

    def truck_h(self, node, linkgraph, penalty):
        for truck, city in node.state[startingPositionsIdx][currTruckIdx]: # (truck, location)
            importantTruck = 0
            for couple in self.goal: # does this truck even appear in the goal
                if couple[0] == truck:
                    importantTruck= 1
                    truckGoalLoc = couple[1]
                    break
            if importantTruck == 0: # if the truck doesn't appear in the goal, skip him
                continue
            if (truck, city) not in self.goal:
                for link in linkgraph.nodesList:
                    personOnTruck = 1
                    if link.name == truckGoalLoc:
                        distLinkDict = bfs(link, node.state[locationIdx])
                        for driver, loc in node.state[startingPositionsIdx][currDriverIdx]:
                            if loc == truck:
                                personOnTruck = 0
                                break
                        penalty = penalty + 5 * personOnTruck + distLinkDict[city]
                        break
        return penalty

    def package_h(self, node, linkgraph, penalty):
        for package, loc in node.state[startingPositionsIdx][currPackIdx]:
            importantPackage = 0
            for couple in self.goal: # (package, location)
                if couple[0] == package:
                    importantPackage = 1
                    packageGoalLoc = couple[1]
                    break
            if importantPackage == 0:
                continue
            if (package, loc) not in self.goal: # package not in goal city / truck yet.
                if loc in node.state[truckIdx]: # current location for package is truck
                    for truck, city in node.state[startingPositionsIdx][currTruckIdx]: # current location of truck is pos
                        if loc == truck:
                            personOnTruck = 1
                            for driver, pos in node.state[startingPositionsIdx][currDriverIdx]:
                                if pos == truck:
                                    personOnTruck = 0
                                    break
                            for link in linkgraph.nodesList:
                                if link.name == packageGoalLoc:
                                    distLinkDict = bfs(link, node.state[locationIdx])
                                    penalty = penalty + distLinkDict[city] + 5 * personOnTruck
                                    break
                else:
                    for link in linkgraph.nodesList:
                        if link.name == packageGoalLoc:
                            distLinkDict = bfs(link, node.state[locationIdx])
                            penalty = penalty + distLinkDict[loc] + 20
                            break
        return penalty


    def h(self, node):
        # """ This is the heuristic. It gets a node (not a state)
        # and returns a goal distance estimate
        # Must return an integer"""
        linkgraph = Graph(linksIdx)
        linkgraph.createGraph(node.state)
        pathgraph = Graph(pathsIdx)
        pathgraph.createGraph(node.state)
        # pathgraph.printGraph()
        penalty = 0
        # for drivers
        print 1
        penalty = self.driver_h(node, linkgraph, pathgraph, penalty)
        # for trucks
        print 2
        penalty = self.truck_h(node, linkgraph, penalty)
        # for packages
        print 3
        penalty = self.package_h(node, linkgraph, penalty)

        return penalty



def create_driverlog_problem(problem):
    goal = problem[-1]
    """ Create a driverlog problem, based on the description.
    problem -- nested tuple as it was described in the description pdf file """

    return DriverlogProblem(problem, goal)
