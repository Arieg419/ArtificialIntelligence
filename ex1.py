import search
import random
import math
import collections
from utils import infinity
from copy import deepcopy

ids = ["302365697"]
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

def bfs(startNode, cities, bfsNodes, typeOfTransport):
    queue = []
    startNode.visited = True
    bfsNodes[startNode.name].visited = True
    queue.append(startNode.name)
    distDict = {}
    for city in cities:
        distDict[city] = float("inf")
    distDict[startNode.name] = 0
    while queue:
        actualNodeName = queue.pop()
        actualNode = bfsNodes[actualNodeName]
        if typeOfTransport == "path":
            for nName in actualNode.pathAdjacenciesList:
                n = bfsNodes[nName]
                if not n.visited:
                    n.visited = True
                    queue.append(n.name)
                    distDict[n.name] = distDict[actualNodeName] + 1
        else:
            for nName in actualNode.linkAdjacenciesList:
                n = bfsNodes[nName]
                if not n.visited:
                    n.visited = True
                    queue.append(n.name)
                    distDict[n.name] = distDict[actualNodeName] + 1
    for nodeName, node in bfsNodes.iteritems():
        bfsNodes[nodeName].visited = False
    # print "start node is ", startNode.name, typeOfTransport
    # for key, val in distDict.iteritems():
    #     print "key val right after bfs ", key, val
    return distDict

class BFSnode:
    def __init__(self, name):
        self.name = name
        self.linkAdjacenciesList = []
        self.pathAdjacenciesList = []
        self.visited = False

    def printAdjacencies(self):
        for neighbor in self.linkAdjacenciesList:
            print neighbor
        for neighbor in self.pathAdjacenciesList:
            print neighbor

class Graph:
    def __init__(self):
        self.nodesList = []
        self.bfsNodes = {}

    def nodeInAdjacenciesList(self, adjlist, city):
        for loc in adjlist:
            if city == loc:
                return True
        return False

    def printBFSNodes(self):
        print "Printing BFS NODES OF GRAPH CLASS: \n"
        for nodeName in self.bfsNodes.keys():
            print "Start node is ", nodeName
            self.bfsNodes[nodeName].printAdjacencies()
            print "END OF BFS NODES OF GRAPH CLASS: \n"


    def createGraph(self, node):
        for city in node[locationIdx]: # ('1', '2', '3')
            currNode = BFSnode(city)
            for link in node[linksIdx]: # link is (origin, destination)
                if link[0] == city and not self.nodeInAdjacenciesList(currNode.linkAdjacenciesList, link[1]):
                    currNode.linkAdjacenciesList.append(link[1])
                if link[1] == city and not self.nodeInAdjacenciesList(currNode.linkAdjacenciesList, link[0]):
                    currNode.linkAdjacenciesList.append(link[0])
            for path in node[pathsIdx]: # link is (origin, destination)
                if path[0] == city and not self.nodeInAdjacenciesList(currNode.pathAdjacenciesList, path[1]):
                    currNode.pathAdjacenciesList.append(path[1])
                if path[1] == city and not self.nodeInAdjacenciesList(currNode.pathAdjacenciesList, path[0]):
                    currNode.pathAdjacenciesList.append(path[0])
            self.nodesList.append(currNode)
            self.bfsNodes[currNode.name] = currNode

    def printGraph(self, str):
        print "********* Printing " , str, " *********\n"
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


        #print "******** END OF SUCCESSOR *************"
        return self.nextStates

    def goal_test(self, state):
        for tupel in self.goal:
            s = state[startingPositionsIdx]
            if tupel not in s[currDriverIdx] and tupel not in s[currTruckIdx] and tupel not in s[currPackIdx]:
                return False
        return True

    def isDriverInSpecificCity(self, state, driverReceived, loc):
        for driver, city in state[startingPositionsIdx][currDriverIdx]:
            if driver == driverReceived and loc == city:
                return True
        return False

    def isDriverInCity(self, state, driverReceived):
        for driver, city in state[startingPositionsIdx][currDriverIdx]:
            if driver == driverReceived:
                return True
        return False

    def doesCityHaveDriver(self, state, cityReceived):
        for driver, city in state[startingPositionsIdx][currDriverIdx]:
            if city == cityReceived:
                return True
        return False

    def trucksInCity(self, state, cityReceived):
        trucks = []
        for truck, city in state[startingPositionsIdx][currTruckIdx]:
            if city == cityReceived:
                trucks.append(truck)
        return trucks

    def isDriverInTruck(self, state, driverReceived):
        for driver, city in state[startingPositionsIdx][currDriverIdx]:
            if driver == driverReceived:
                return True
        return False

    def doesTruckHaveDriver(self, state, truckReceived):
        for driver, truck in state[startingPositionsIdx][currDriverIdx]:
            if truck == truckReceived:
                return True
        return False

    def isItemImportant(self, entity):
        for item, loc in self.goal:
            if item == entity:
                return True, loc
        return False, ""

    def inGoalState(self, item, goal):
        return True if item in goal else False

    def locIsTruck(self, loc, truckLocations):
        return True if loc in truckLocations else False

    def findCityOfTruck(self, loc, currentPositions):
        for truck, city in currentPositions:
            if truck == loc:
                return city

    def doesCityHaveTruck(self, loc, state):
        for truck, city in state[startingPositionsIdx][currTruckIdx]:
            if city == loc:
                return True
        return False

    def maxValInDict(self, dictionary):
        maxVal = 0
        maxKey = 0
        for key in dictionary.keys():
            if dictionary[key] > maxVal and not math.isinf(dictionary[key]):
                maxVal = dictionary[key]
                maxKey = key
        return maxKey

        ###### Avg Calc ###########
        # values = []
        # for key, val in dictionary.iteritems():
        #     values.append(val)
        # values.sort()
        # for key, val in dictionary.iteritems():
        #     if val == values[len(values)/2]:
        #         return key
        # return -1
        ############################

    def driver_h(self, node, graph, penalty):
        for driver, loc in node.state[startingPositionsIdx][currDriverIdx]: # (driver, location) or (driver,truck)
            important = self.isItemImportant(driver)  # (True/False, loc/"")
            if not important[0]:
                continue
            driverGoalLoc = important[1]
            pathPenalty = 0
            linkPenalty = 0
            if (driver, loc) not in self.goal:
                if loc in node.state[locationIdx]: # if the driver is currently in a city
                    # do bfs on Graph to find distance between loc and driverGoalLoc
                    for gnode in graph.nodesList:
                        if gnode.name == loc:
                            distPathDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "path")
                            pathPenalty = penalty + distPathDict[driverGoalLoc]
                            distLinkDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "link")
                            if self.doesCityHaveTruck(loc, node.state):
                                linkPenalty = penalty + distLinkDict[driverGoalLoc] + 6
                            else:
                                #  bring truck through links
                                maxkey = self.maxValInDict(distLinkDict)
                                if maxkey == 0:
                                    linkPenalty = penalty + distLinkDict[driverGoalLoc] + 100 + 1
                                else:
                                    linkPenalty = penalty + distLinkDict[driverGoalLoc] + distLinkDict[maxkey] + 6
                            penalty = max(linkPenalty, pathPenalty)
                            break
                else:  # driver is currently in truck, # find what city the truck is in
                    for truck, city in node.state[startingPositionsIdx][currTruckIdx]:
                        if truck == loc:
                            # do bfs on Graph to find distance between city and driverGoalLoc + penalty
                            for gnode in graph.nodesList:
                                if gnode.name == city:
                                    distPathDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "path")
                                    pathPenalty = penalty + distPathDict[driverGoalLoc] + 6
                                    distLinkDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "link")
                                    linkPenalty = penalty + distLinkDict[driverGoalLoc] + 6
                                    penalty = max(linkPenalty, pathPenalty)
                                    break
        return penalty

    def truck_h(self, node, graph, penalty):
        for truck, city in node.state[startingPositionsIdx][currTruckIdx]:  # (truck, location)
            pathPenalty = 0
            linkPenalty = 0
            important = self.isItemImportant(truck)  # (True/False, loc/"")
            if not important[0]:
                continue
            truckGoalLoc = important[1]
            if (truck, city) not in self.goal:
                for gnode in graph.nodesList:  # bring driver via links
                    if gnode.name == city:
                        # print "bfs w/ link graph "
                        distLinkDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "link")
                        if not self.doesTruckHaveDriver(node.state, truck):
                            #  bring driver through links
                            maxkeyLink = self.maxValInDict(distLinkDict)
                            if maxkeyLink == 0:
                                linkPenalty = penalty + distLinkDict[truckGoalLoc] + 100 + 2
                            else:
                                linkPenalty = penalty + distLinkDict[truckGoalLoc] + distLinkDict[maxkeyLink] + 7
                            #  bring driver through paths
                            distPathDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "path")
                            maxkeyPath = self.maxValInDict(distPathDict)
                            if maxkeyPath == 0:
                                pathPenalty = penalty + distLinkDict[truckGoalLoc] + 100
                            else:
                                pathPenalty = penalty + distLinkDict[truckGoalLoc] + distPathDict[maxkeyLink] + 5
                        else:
                            linkPenalty = penalty + distLinkDict[truckGoalLoc]
                        penalty = max(linkPenalty, pathPenalty)
                        break
        return penalty


    def package_h(self, node, graph, penalty):
        for package, loc in node.state[startingPositionsIdx][currPackIdx]:
            important = self.isItemImportant(package)  # (True/False, loc/"")
            if not important[0]:
                continue
            packageGoalLoc = important[1]
            pathPenalty = 0
            linkPenalty = 0
            if not self.inGoalState((package, loc), self.goal):  # package not in goal city / truck yet.
                if self.locIsTruck(loc, node.state[truckIdx]):  # current location for package is truck
                    for truck, city in node.state[startingPositionsIdx][currTruckIdx]:
                        if loc == truck:  # the truck the package is on
                            city = self.findCityOfTruck(loc, node.state[startingPositionsIdx][currTruckIdx])
                            for gnode in graph.nodesList:
                                if gnode.name == city:
                                    distLinkDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "link")
                                    if not self.doesTruckHaveDriver(node.state, truck):
                                        # bring driver through links
                                        maxkeyLink = self.maxValInDict(distLinkDict)
                                        if maxkeyLink == 0:
                                            linkPenalty = penalty + distLinkDict[packageGoalLoc] + 100 + 2
                                        else:
                                            linkPenalty = penalty + distLinkDict[packageGoalLoc]+ distLinkDict[maxkeyLink] + 7
                                        # bring driver through paths
                                        distPathDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "path")
                                        maxkeyPath = self.maxValInDict(distLinkDict)
                                        if maxkeyPath == 0:
                                            pathPenalty = penalty + distLinkDict[packageGoalLoc] + 100
                                        else:
                                            pathPenalty = penalty + distLinkDict[packageGoalLoc] + distPathDict[maxkeyPath] + 5
                                    else:
                                        linkPenalty = penalty + distLinkDict[packageGoalLoc] + 6
                                    penalty = max(linkPenalty, pathPenalty)
                                    break

                else:  # current loc of package is city
                    for gnode in graph.nodesList:
                        if gnode.name == loc:
                            distLinkDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "link")
                            trucks = self.trucksInCity(node.state, loc)
                            truckWithDriver = 0
                            for truck in trucks:
                                if self.doesTruckHaveDriver(node.state, truck):
                                    truckWithDriver = 1
                            if truckWithDriver == 1:  # there's at least one truck with a driver
                                linkPenalty = penalty + distLinkDict[packageGoalLoc] + 7
                            elif len(trucks) == 0:  # there are no trucks in city
                                maxkey = self.maxValInDict(distLinkDict)
                                if maxkey == 0:
                                    linkPenalty = penalty + 100 + distLinkDict[packageGoalLoc] + 7
                                else:
                                    linkPenalty = penalty + 2 * distLinkDict[maxkey] + distLinkDict[packageGoalLoc] + 7
                            else:  # there are only trucks with no drivers in city
                                # bring driver though link
                                maxkeyLink = self.maxValInDict(distLinkDict)
                                if maxkeyLink == 0:
                                    linkPenalty = penalty + 100 + distLinkDict[packageGoalLoc] + 2
                                else:
                                    linkPenalty = penalty + distLinkDict[maxkeyLink] + distLinkDict[packageGoalLoc] + 7
                                #bring driver through paths
                                distPathDict = bfs(gnode, node.state[locationIdx], graph.bfsNodes, "path")
                                maxkeyPath = self.maxValInDict(distLinkDict)
                                if maxkeyPath == 0:
                                    pathPenalty = penalty + 100 + distPathDict[packageGoalLoc] + 2
                                else:
                                    pathPenalty = penalty + distPathDict[maxkeyPath] + distLinkDict[packageGoalLoc] + 6
                            penalty = max(linkPenalty, pathPenalty)
                            break
        return penalty


    def h(self, node):
        # """ This is the heuristic. It gets a node (not a state)
        # and returns a goal distance estimate
        # Must return an integer"""
        graph = Graph()
        graph.createGraph(node.state)
        # graph.printGraph("Link Graph")
        # graph.printBFSNodes()
        penalty = 0
        # for drivers
        # print 1
        penalty = self.driver_h(node, graph, penalty)
        # for trucks
        # print 2
        penalty = self.truck_h(node, graph, penalty)
        # for packages
        # print 3
        penalty = self.package_h(node, graph, penalty)

        return penalty
        # return 0



def create_driverlog_problem(problem):
    goal = problem[-1]
    """ Create a driverlog problem, based on the description.
    problem -- nested tuple as it was described in the description pdf file """

    return DriverlogProblem(problem, goal)
