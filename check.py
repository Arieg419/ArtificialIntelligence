import ex1
import search
import time

def timeout_exec(func, args=(), kwargs={}, timeout_duration=10, default=None):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """ 
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as e:    
                self.result = (-3, -3, e)
            
    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return default
    else:
        return it.result

def check_problem(p, search_method, timeout):    
    """ Constructs a problem using ex1.create_driverlog_problem,
    and solves it using the given search_method with the given timeout.
    Returns a tuple of (solution length, solution time, solution)
    (-2, -2, None) means there was a timeout
    (-3, -3, ERR) means there was some error ERR during search"""        
    
    
    t1 = time.time()
    s = timeout_exec(search_method, args=[p], timeout_duration=timeout)
    t2 = time.time()
    
    if isinstance(s, search.Node):
        solve = s
        solution = map(lambda n: n.action, solve.path()[::-1])[1:]
        return (len(solution), t2 - t1, solution)
    elif s is None:
        return (-2, -2, None)
    else:        
        return s
    

def solve_problems(problem):
    solved = 0
    print "PROBLEM: "
    definitions = ("Drivers:", "Trucks:", "Packages:","Locations:", "Links:", "Paths:", "Starting positions:", "Goal:")
    to_print = zip(definitions, problem)
    for row in to_print:
        for c in row:
            print c,
        print
    
         
    try:
        p = ex1.create_driverlog_problem(problem)
    except Exception as e:
        print "Error creating problem: ", e
        return None
    timeout = 60
    result = check_problem(p, (lambda p: search.best_first_graph_search(p, p.h)), timeout)
    print "GBFS ", result
    if result[2] != None:
        solved = solved + 1
    result = check_problem(p, search.astar_search, timeout)
    print "A*   ", result        
    result = check_problem(p, search.breadth_first_graph_search, timeout)
    # print "BFSg ", result
    # result = check_problem(p, search.breadth_first_tree_search, timeout)
    # print "BFSt ", result
    # result = check_problem(p, search.depth_first_graph_search, timeout)
    # print "DFSg ", result
    # result = check_problem(p, search.depth_first_tree_search, timeout)
    # print "DFSt ", result
    # result = check_problem(p, search.iterative_deepening_search, timeout)
    
    print "GBFS Solved ", solved

    
def main():
    print ex1.ids
    problem=(("harry", "ron", "hermione", "lilly potter"),
        ("isuzu", "mazda", "subaru", "jeep"),
        ("a", "b", "c", "d"),
        ("1", "2", "3", "4"),
        (("1", "2"), ("2", "3"), ("1", "3"), ("1", "4"), ("2", "4"), ("3", "4"),),
        (("1", "2"), ("2", "3"), ("1", "3"), ("1", "4"), ("2", "4"), ("3", "4"),),
        ((("harry", "isuzu"), ("ron", "mazda"), ("hermione", "subaru"), ("lilly potter", "1")), (("isuzu", "2"),
            ("mazda", "3"), ("jeep", "1"), ("subaru", "4")), (("a", "isuzu"), ("b", "mazda"), ("c", "3"), ("d", "4"))),
        (("a", "2"), ("b", "3"), ("c", "4"), ("d", "1")))
    solve_problems(problem)
    
if __name__ == '__main__':
    main()
