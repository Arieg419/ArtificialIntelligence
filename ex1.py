import search
import math

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
        """Don't forget to set the goal or implement the goal test"""
        self.goal = goal
        search.Problem.__init__(self, initial, goal)

    def printCitiesInDict(self, state, cityDictionary):
        print "*************************** CitiesDict ***************************"
        for idx, val in enumerate(cityDictionary):
            print "********************* City ", val , "*********************\n" 
            print "Drivers: " , cityDictionary[val]["Drivers"], "\n"
            print "Trucks: " , cityDictionary[val]["Trucks"], "\n"
            print "Packages: " , cityDictionary[val]["Packages"], "\n"
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
        
    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework.
        Must return a sequence of (action, state) pairs"""
        global builtCityDict
        if builtCityDict == False:
            self.addCitiesToDict(state)
            self.mapStartingPosToCityDict(state)
            builtCityDict = True
            self.printCitiesInDict(state, cityDictionary)

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state, compares to the created goal state
        Must return a boolean"""

        
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
