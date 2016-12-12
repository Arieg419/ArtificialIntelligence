import search
import math
from copy import deepcopy

ids=["111111111","111111111"]
cityDictionary = {}
builtCityDict = False
keysForCities = ["Drivers","Trucks", "Packages"]
locationIdx = 3
linksIdx = 4
pathsIdx = 5
startingPositionsIdx = 6
goalIdx = 7



# inherits from search.Problem
class DriverlogProblem(search.Problem):
    def __init__(self, initial, goal):
        self.goal = goal
        self.nextStates = []
        search.Problem.__init__(self, initial, goal)
        self.stateRep = ["Drivers: ", "Trucks", "Packages: ", "Locations: ", "Links: ", "Path: ", "Starting Position: ", "Goal: "]

    def printState(self, state):
        print "********&&&&&&&&&&& PrintState Function ********&&&&&&&&&&& "
        for i,item in enumerate(state):
            print self.stateRep[i], item, "\n"
        print "********&&&&&&&&&&& PrintState Function End ********&&&&&&&&&&& "

    def grabCurrentState(self, state):
        print "********&&&&&&&&&&& GRAB CURRENT STATE ********&&&&&&&&&&& "
        print state[6]
        print "********&&&&&&&&&&& GRAB CURRENT STATE ********&&&&&&&&&&& "
    

    def printCitiesInDict(self, state, cityDictionary):
        print "*************************** CitiesDict ***************************"
        for idx, val in enumerate(cityDictionary):
            print "********************* City ", val , "*********************\n" 
            print "Drivers: " , cityDictionary[val]["Drivers"], "\n"
            print "Trucks: " , cityDictionary[val]["Trucks"], "\n"
            print "Packages: " , cityDictionary[val]["Packages"], "\n"
            print "PackagesOnTrucks: " , cityDictionary[val]["PackagesOnTrucks"], "\n"
            print "Links: " , cityDictionary[val]["Links"], "\n"
            print "Paths: " , cityDictionary[val]["Paths"], "\n"
            print "********************* City ", val , " End *********************\n" 
        print "*************************** CitiesDict End ***********************"

    def addCitiesToDict(self, state):
        for idx in range(len(state[locationIdx])):
            cityDictionary[state[locationIdx][idx]] = {
                                                        "Drivers": [],
                                                        "Trucks": [],
                                                        "Packages": [],
                                                        "PackagesOnTrucks": {},
                                                        "DriversOnTrucks": {},
                                                        "Links": [],
                                                        "Paths": []
                                                      }
        
    def mapStartingPosToCityDict(self, state):
        # Adding Drivers, Trucks and Packages to CityDictionary
        for key, item in enumerate(state[startingPositionsIdx]):
            for i, (identifier, city) in enumerate(state[startingPositionsIdx][key]):
                cityDictionary[city][keysForCities[key]].append(identifier)

        # Adding Links to CityDictionary
        for key, item in enumerate(state[linksIdx]):
            origin, destination = state[linksIdx][key]
            cityDictionary[origin]["Links"].append(destination)

        # Adding Paths to CityDictionary
        for key, item in enumerate(state[pathsIdx]):
            origin, destination = state[pathsIdx][key]
            cityDictionary[origin]["Paths"].append(destination)

        # Adding Trucks to Packages on Trucks dictionary
        for key, item in enumerate(state[pathsIdx]):
            origin, destination = state[pathsIdx][key]
            for truck in cityDictionary[origin]["Trucks"]:
                cityDictionary[origin]["PackagesOnTrucks"][truck] = []


    def compute_load_truck_moves(self, state, cityDictionary):
        print 1
        tmpState = list(deepcopy(state))
        # self.printState(tmpState)
        print tmpState
        tmpState[6] = list(tmpState[6]) #problem
        print 7
        tmpState[6][2] = list(tmpState[6][2])
        for idx, val in enumerate(cityDictionary):
            print 2
            if len(cityDictionary[val]["Trucks"]) == 0 or len(cityDictionary[val]["Packages"]) == 0:
                print "City " + val + " Cannot load packages to truck"
            for package in state[6][2]: #('a', '1')
                print 3
                if package[0] in cityDictionary[val]["Packages"]:
                    print 4
                    tmpState[6][2].remove(package)
                    for truck in cityDictionary[val]["Trucks"]:
                        print 5
                        tmpState[6][2].append((package[0], truck))
                        tmpState[6][2] = tuple(tmpState[6][2]) # package and goal state
                        tmpState[6] = tuple(tmpState[6])
                        tmpState = tuple(tmpState)
                        #cityDictionary[val]["PackagesOnTrucks"][truck].append(package[0])
                        yield ("load_truck", package[0], truck), (tmpState[6])  
                    print 6
                    tmpState = list(tmpState)
                    tmpState[6] = list(tmpState[6])
                    tmpState[6][2] = list(tmpState[6][2])
                    tmpState[6][2].append(package)

    # TODO - how am i supposed to keep track of who is on what truck? This is based on the algos decision
    # For all trucks in city
        # Check which packages are on trucks
        # Unload them and add to current city
        # Yield new state
    def compute_unload_truck_moves(self, state, cityDictionary):
        tmpState = list(state)
        tmpState[2] = list(tmpState[2])
        for idx, val in enumerate(cityDictionary):
            print "********************* City ", val , "Unloading truck", "*********************\n" 
            if len(cityDictionary[val]["PackagesOnTrucks"]) == 0:
                print "No Packages to unload"
            for truck in cityDictionary[val]["PackagesOnTrucks"]:
                    if len(cityDictionary[val]["PackagesOnTrucks"][truck]) != 0:
                        for package in cityDictionary[val]["PackagesOnTrucks"][truck]:
                            print "Printing my fing list", cityDictionary[val]["PackagesOnTrucks"][truck], package
                            cityDictionary[val]["PackagesOnTrucks"][truck].remove(package)
                            # TODO, for not iterating over all items in list
                            #if package not in cityDictionary[val]["Packages"]:
                            #    cityDictionary[val]["Packages"].append(package)
                            #    print "Appeneded"
                            # Updating State of World
                            #self.nextStates.append("Load truck " + truck + " with package " + package , ())
            print "************ ENDING CITY " + val + " TRUCK UNLOAD **************"

    def compute_board_truck_moves(self, state, cityDictionary):
        tmpState = list(state)
        tmpState[6] = list(tmpState[6])
        tmpState[6][0] = list(tmpState[6][0])
        for idx, val in enumerate(cityDictionary):
            if len(cityDictionary[val]["Trucks"]) == 0 or len(cityDictionary[val]["Drivers"]) == 0:
                print "City " + val + " Cannot board driver to truck"
            for driver in state[6][0]:
                if driver[0] in cityDictionary[val]["Drivers"]:
                    tmpState[6][0].remove(driver)
                    tmpState[6][0] = tuple(tmpState[6][0])
                    tmpState[6] = tuple(tmpState[6])
                    tmpState = tuple(tmpState)
                    for truck in cityDictionary[val]["Trucks"]:
                        yield (("board_truck " + driver[0] + " "+ truck), (tmpState))   
                    tmpState = list(tmpState)
                    tmpState[6] = list(tmpState[6])
                    tmpState[6][0] = list(tmpState[6][0])
                    tmpState[6][0].append(driver)

    def compute_disembark_truck_moves(self, state, cityDictionary):
        # TODO How do i save passengers on trucks into the state? How do I know what action the algorithm selected?
        # This is the only way to update state accoridingly
        yield "yaya"

    def compute_drive_truck_moves(self, state, cityDictionary):
        tmpState = list(state)
        tmpState[6] = list(tmpState[6])
        tmpState[6][1] = list(tmpState[6][1])
        for idx, val in enumerate(cityDictionary):
            # TODO Will need to check for people on trucks as well, needed criteria for driving
            if len(cityDictionary[val]["Trucks"]) == 0 or len(cityDictionary[val]["Links"]) == 0:
                print "City " + val + " Cannot drive truck via Link"
            for truck in state[6][1]:
                if truck[0] in cityDictionary[val]["Trucks"]:
                    for link in cityDictionary[val]["Links"]:
                        tmpState[6][1].remove(truck)
                        tmpState[6][1].append((truck[0], link))
                        tmpState[6][1] = tuple(tmpState[6][1])
                        tmpState[6] = tuple(tmpState[6])
                        tmpState = tuple(tmpState)
                        yield (("drive_truck " + truck[0] + " " + truck[1] + " " + link), (tmpState))   
                        tmpState = list(tmpState)
                        tmpState[6] = list(tmpState[6])
                        tmpState[6][1] = list(tmpState[6][1])
                        tmpState[6][1].remove((truck[0], link))
                        tmpState[6][1].append(truck)

    def compute_walk_moves(self, state, cityDictionary):
        tmpState = list(state)
        tmpState[6] = list(tmpState[6])
        tmpState[6][0] = list(tmpState[6][0])
        for idx, val in enumerate(cityDictionary):
            if len(cityDictionary[val]["Drivers"]) == 0 or len(cityDictionary[val]["Paths"]) == 0:
                print "City " + val + " Cannot walk driver via Path"
            for driver in state[6][0]:
                if driver[0] in cityDictionary[val]["Drivers"]:
                    for path in cityDictionary[val]["Paths"]:
                        tmpState[6][0].remove(driver)
                        tmpState[6][0].append((driver[0], path))
                        tmpState[6][0] = tuple(tmpState[6][0])
                        tmpState[6] = tuple(tmpState[6])
                        tmpState = tuple(tmpState)
                        yield (("walk " + driver[0] + " " + driver[1] + " " + path), (tmpState))   
                        tmpState = list(tmpState)
                        tmpState[6] = list(tmpState[6])
                        tmpState[6][0] = list(tmpState[6][0])
                        tmpState[6][0].remove((driver[0], path))
                        tmpState[6][0].append(driver)
        

    def successor(self, state):
        global builtCityDict
        if builtCityDict == False:
            self.addCitiesToDict(state)
            self.mapStartingPosToCityDict(state)
            self.printCitiesInDict(state, cityDictionary)
            builtCityDict = True

        currState = self.grabCurrentState(state)
        print currState


        for act, newState in self.compute_load_truck_moves(state, cityDictionary):
            self.nextStates.append((act, newState))
            #print self.nextStates
            yield [act, newState]

        #print "last print !!!!!!!!!!"
        #print self.nextStates
        #for item in self.nextStates:
        #    print item

        #for item in self.compute_unload_truck_moves(state, cityDictionary):
            #print item
            #    append to self.nextState
        #    print "\n"

        # for item in self.compute_board_truck_moves(state, cityDictionary):
        #     # TODO do i need to return the whole world information, or only new positions?
        #     self.nextStates.append(item)

        # for item in self.compute_drive_truck_moves(state, cityDictionary):
        #     self.nextStates.append(item)

        # for item in self.compute_walk_moves(state, cityDictionary):
        #     # TODO do i need to return the whole world information, or only new positions?
        #     self.nextStates.append(item)
            

        # #return self.nextStates
        # for item in self.nextStates:
        #     print item, "\n"

        # return [("load_truck", "a",'isuzu'), (state)]


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
