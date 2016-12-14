import search
import math
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

    def grabCurrentState(self, state):
        return state[6]

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
            self.cityDictionary[origin]["Links"].append(destination)

        # Adding Paths to CityDictionary
        for key, item in enumerate(state[pathsIdx]):
            origin, destination = state[pathsIdx][key]
            self.cityDictionary[origin]["Paths"].append(destination)

    def compute_load_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[2] = list(deepcopy(newState[2]))  # problem
        for idx, val in enumerate(cityDictionary):
            # check that we are not iterating over a truck
            if val in self.origState[1]:
                continue
            if len(cityDictionary[val]["Trucks"]) == 0 or len(cityDictionary[val]["Packages"]) == 0:
                continue
            for package in state[2]:  # ('a', '1')
                if package[0] in cityDictionary[val]["Packages"]:
                    newState[2].remove(package)
                    for truck in cityDictionary[val]["Trucks"]:
                        if ("load_truck", package[0], truck) in self.newActions:
                            continue
                        newState[2].append((package[0], truck))
                        newState[2] = tuple(deepcopy(newState[2]))
                        newState = tuple(deepcopy(newState))
                        self.newActions.append(("load_truck", package[0], truck))
                        yield ("load_truck", package[0], truck), (newState)  # act, state
                    newState = list(newState)
                    newState[2] = list(newState[2])
                    # newState[2].append(package) do i need this?
                    # Yield new state

    def compute_unload_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[2] = list(deepcopy(newState[2])) # package car list
        for idx, truck in enumerate(cityDictionary):
            if truck not in self.origState[1]: # only for trucks
                continue
           # print "********************* Location ", truck, "Unloading truck", "*********************\n"
            for package in state[2]:
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
            #print "************ ENDING CITY " + truck + " TRUCK UNLOAD **************"

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
                        if ("board_truck ", driver[0], truck) in self.newActions:
                            continue
                        self.newActions.append(("board_truck ", driver[0], truck))
                        newState[0].remove(driver)
                        newState[0].append((driver[0], truck))
                        newState[0] = tuple(deepcopy(newState[0]))
                        newState = tuple(deepcopy(newState))
                        yield ("board_truck ", driver[0], truck), (newState)
                        newState = list(newState)
                        newState[0] = list(newState[0])

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
                    if ("disembark_truck ", driver[0], truck) in self.newActions:
                        continue
                    truckLocation = cityDictionary[truck]["Location"]
                    self.newActions.append(("disembark_truck ", driver[0], truck))
                    newState[0].remove(driver)
                    newState[0].append((driver[0], truckLocation))
                    newState[0] = tuple(deepcopy(newState[0]))
                    newState = tuple(deepcopy(newState))
                    yield ("disembark_truck ", driver[0], truck), (newState)
                    newState = list(newState)
                    newState[0] = list(newState[0])

    def compute_drive_truck_moves(self, state, cityDictionary):
        newState = list(deepcopy(state))
        newState[0] = list(deepcopy(state[0])) # list of driver positions
        for idx, truck in enumerate(cityDictionary):
            if truck not in self.origState[1]: # only on trucks
                continue
            if len(cityDictionary[truck]["Drivers"]) == 0:
                continue
            for driver in state[0]: # driver is (driver, truck)
                if driver[0] in cityDictionary[truck]["Drivers"]:
                    truckLocation = cityDictionary[truck]["Location"]
                    for link in cityDictionary[truckLocation]["Links"]:
                        if ("drive_truck ", truck, truckLocation, link) in self.newActions:
                            continue
                        self.newActions.append(("drive_truck ", truck, truckLocation, link))
                        newState[0].remove(driver) # TODO, this remove fails
                        newState[0].append((truck, link))
                        newState[0] = tuple(deepcopy(newState[0]))
                        newState = tuple(deepcopy(newState))
                        yield (("drive_truck ", truck, truckLocation, link), (newState))
                        newState = list(newState)
                        newState[0] = list(newState[0])

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
                    for path in cityDictionary[city]["Links"]:
                        print "************** PATH TIME *****************", path
                        if ("walk ", driver[0], city, path) in self.newActions:
                            continue
                        self.newActions.append(("walk ", driver[0], city, path))
                        newState[0].remove(driver) # checked remove here on list, all good :)
                        newState[0].append((driver[0], path))
                        newState[0] = tuple(deepcopy(newState[0]))
                        newState = tuple(deepcopy(newState))
                        yield (("walk ", driver[0], city, path), (newState))
                        newState = list(newState)
                        newState[0] = list(newState[0])

    def successor(self, state):
        global builtCityDict
        self.origState = state
        if builtCityDict == False:
            self.addCitiesToDict(state)
            self.mapStartingPosToCityDict(state)
            self.printingTrucksInDict(state, self.cityDictionary)
            self.printCitiesInDict(state, self.cityDictionary)
            builtCityDict = True

        currState = self.grabCurrentState(state)

        # TODO nextStates should clean itself before every successor run, or should only run once for all search algo (GBFS, A*,etc..)
        # TODO optimization, destructure currState and only passs relevant data to function
        for act, newState in self.compute_load_truck_moves(currState, self.cityDictionary):
           self.nextStates.append((act, newState))


        for act, newState in self.compute_unload_truck_moves(currState, self.cityDictionary):
          self.nextStates.append((act, newState))


        for act, newState in self.compute_board_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, newState))

        for act, newState in self.compute_disembark_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, newState))

        # TODO, remove function causes error to be thrown
        for act, newState in self.compute_drive_truck_moves(currState, self.cityDictionary):
            self.nextStates.append((act, newState))

        # TODO, does not offer walk 1, 3 although we see it being created in debug mode. it is removed some time later.
        for act, newState in self.compute_walk_moves(currState, self.cityDictionary):
            self.nextStates.append((act, newState))

        print "*************************** NewState before yield *******************************"
        for item in self.nextStates:
            print item, "\n"
        print "*************************** END NewState before yield *******************************"
        return self.nextStates

            # print "last print !!!!!!!!!!"
            # print self.nextStates
            # for item in self.nextStates:
            #    print item



            # for item in self.compute_walk_moves(state, cityDictionary):
            #     # TODO do i need to return the whole world information, or only new positions?
            #     self.nextStates.append(item)


            # #return self.nextStates
            # for item in self.nextStates:
            #     print item, "\n"

    def goal_test(self, state):
        if state == self.goal:
            return True
        return False

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate
        Must return an integer"""
        """
        Every search function - astar, BFS, DFS etc. - gets a successor function output.
        It then uses the heuristic function for all possible new states, and picks the 
        move that has the best heuristic output
        """
        return 0


'''
This is the driverlog type
problem=(("jon", "sansa"),
            ("isuzu", "mazda"),
            ("a", "b"),
            ("1", "2"),
            (("1", "2"),),
            (),
            ((("jon", "1"), ("sansa", "1")), (("isuzu", "1"), ("mazda", "2")), (("a", "1"), ("b", "2"))),
            (("a", "2"), ("b", "1")))
'''


def create_driverlog_problem(problem):
    goal = problem[-1]
    """ Create a driverlog problem, based on the description.
    problem -- nested tuple as it was described in the description pdf file """

    return DriverlogProblem(problem, goal)
