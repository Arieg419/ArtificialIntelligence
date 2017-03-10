import ex1
import search
import time

problems = []
problem1 = (("frodo",),
            ("isuzu",),
            ("the_ring",),
            ("shire", "2", "3", "4", "5", "mount_doom"),
            (("shire", "2"), ("2", "3"), ("3", "4"), ("4", "5"), ("5", "mount_doom")),
            (("shire", "4"), ("3", "mount_doom")),
            ((("frodo", "shire"),), (("isuzu", "shire"),), (("the_ring", "shire"),)),
            (("the_ring", "mount_doom"), ("isuzu", "shire")))
problems.append(problem1)
problem2 = (("tyrion", "cercei"),
            ("isuzu",),
            ("a", "b"),
            ("1", "2", "3"),
            (("1", "2"), ("2", "3")),
            (("1", "3"),),
            ((("tyrion", "1"), ("cercei", "isuzu")), (("isuzu", "1"),), (("a", "isuzu"), ("b", "3"))),
            (("a", "2"), ("b", "2")))
problems.append(problem2)
problem3 = (("jon",),
            ("isuzu",),
            ("a",),
            ("1", "2"),
            (("1", "2"),),
            (),
            ((("jon", "1"),), (("isuzu", "1"),), (("a", "1"),)),
            (("a", "2"),))
problems.append(problem3)
problem4 = (("jon", "sansa"),
            ("isuzu", "mazda"),
            ("a", "b"),
            ("1", "2"),
            (("1", "2"),),
            (),
            ((("jon", "1"), ("sansa", "1")), (("isuzu", "1"), ("mazda", "2")), (("a", "1"), ("b", "2"))),
            (("a", "2"), ("b", "1")))
problems.append(problem4)
problem5 = (("frodo",),
            ("isuzu",),
            ("the_ring",),
            ("shire", "2", "3", "4", "5", "mount_doom"),
            (("shire", "2"), ("2", "3"), ("3", "4"), ("4", "5"), ("5", "mount_doom")),
            (("shire", "4"), ("3", "mount_doom")),
            ((("frodo", "shire"),), (("isuzu", "shire"),), (("the_ring", "shire"),)),
            (("the_ring", "mount_doom"), ("isuzu", "shire")))
problems.append(problem5)
problem6 = (("harry", "ron", "hermione"),
            ("isuzu", "mazda", "subaru"),
            ("a", "b", "c", "d"),
            ("1", "2", "3", "4"),
            (("1", "2"), ("2", "3"), ("1", "3"), ("1", "4"), ("2", "4"), ("3", "4"),),
            (("1", "2"), ("2", "3"), ("1", "3"), ("1", "4"), ("2", "4"), ("3", "4"),),
            ((("harry", "1"), ("ron", "2"), ("hermione", "3")), (("isuzu", "2"), ("mazda", "3"), ("subaru", "4")),
             (("a", "1"), ("b", "2"), ("c", "3"), ("d", "4"))),
            (("a", "2"), ("b", "3"), ("c", "4"), ("d", "1")))
problems.append(problem6)
problem7 = (('linda', 'william'),
            ('hyundai', 'chevrolet'),
            ('f', 'h', 'l'),
            ('1', '2', '3', '4', '5'),
            (('1', '2'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '4'), ('3', '1'), ('3', '2'), ('3', '4'), ('4', '1'),
             ('4', '2'), ('4', '3'), ('4', '5'), ('5', '1'), ('5', '2'), ('5', '3')),
            (('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '1'), ('2', '4'), ('2', '5'), ('3', '1'), ('3', '2'),
             ('3', '5'), ('4', '2'), ('4', '3'), ('4', '5'), ('5', '1'), ('5', '2'), ('5', '4')),
            ((('linda', '3'), ('william', '3')), (('hyundai', '4'), ('chevrolet', '5')),
             (('f', '4'), ('h', '1'), ('l', '5'))),
            (('hyundai', '3'), ('f', '4')))
problems.append(problem7)
problem8 = (('john', 'barbara'),
            ('daewoo', 'isuzu'),
            ('o', 'j', 'e'),
            ('1', '2', '3', '4', '5'),
            (('1', '2'), ('1', '4'), ('2', '1'), ('2', '4'), ('2', '5'), ('3', '1'), ('3', '2'), ('3', '4'), ('4', '1'),
             ('4', '2'), ('4', '3'), ('5', '1'), ('5', '2'), ('5', '3'), ('5', '4')),
            (('1', '3'), ('2', '1'), ('2', '3'), ('2', '5'), ('3', '1'), ('3', '4'), ('3', '5'), ('4', '1'), ('4', '2'),
             ('4', '5'), ('5', '1'), ('5', '2'), ('5', '3')),
            (
            (('john', '2'), ('barbara', '5')), (('daewoo', '3'), ('isuzu', '3')), (('o', '5'), ('j', '2'), ('e', '3'))),
            (('daewoo', '5'), ('j', '1')))
problems.append(problem8)
problem9 = (('robert', 'james', 'patricia', 'mary'),
            ('chevrolet', 'honda', 'isuzu', 'hyundai'),
            ('l', 's', 'd', 'k', 'q', 'o'),
            ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (
            ('1', '2'), ('1', '4'), ('1', '9'), ('1', '10'), ('2', '6'), ('2', '8'), ('3', '1'), ('3', '4'), ('3', '6'),
            ('3', '10'), ('4', '1'), ('4', '2'), ('4', '9'), ('5', '2'), ('5', '4'), ('5', '7'), ('5', '10'),
            ('6', '7'), ('6', '8'), ('6', '10'), ('7', '9'), ('8', '1'), ('8', '2'), ('8', '4'), ('8', '7'), ('9', '1'),
            ('9', '3'), ('9', '4'), ('9', '10'), ('10', '3'), ('10', '5'), ('10', '8')),
            (
            ('1', '2'), ('1', '8'), ('1', '9'), ('1', '10'), ('2', '1'), ('3', '4'), ('3', '7'), ('3', '8'), ('3', '9'),
            ('3', '10'), ('4', '1'), ('4', '2'), ('4', '5'), ('4', '6'), ('4', '7'), ('4', '8'), ('4', '9'), ('5', '2'),
            ('5', '3'), ('5', '6'), ('6', '8'), ('6', '10'), ('7', '2'), ('7', '4'), ('7', '9'), ('7', '10'),
            ('8', '1'), ('8', '2'), ('8', '4'), ('8', '5'), ('8', '6'), ('8', '9'), ('8', '10'), ('9', '1'), ('9', '4'),
            ('9', '5'), ('9', '6'), ('9', '8'), ('9', '10'), ('10', '1'), ('10', '2'), ('10', '4'), ('10', '8')),
            ((('robert', '9'), ('james', '5'), ('patricia', '7'), ('mary', '5')),
             (('chevrolet', '1'), ('honda', '5'), ('isuzu', '9'), ('hyundai', '5')),
             (('l', '1'), ('s', '1'), ('d', '10'), ('k', '8'), ('q', '7'), ('o', '3'))),
            (('q', '10'), ('d', '5'), ('o', '5'), ('isuzu', '5')))
problems.append(problem9)
problem10 = (('james', 'william', 'patricia', 'barbara'),
('sierra', 'isuzu', 'chevrolet', 'ford'),
('p', 'n', 'd', 's', 'l', 'j'),
('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
(('1', '8'), ('1', '10'), ('2', '1'), ('2', '3'), ('2', '5'), ('2', '7'), ('2', '8'), ('3', '2'), ('3', '5'), ('3', '7'), ('3', '8'), ('3', '10'), ('4', '5'), ('4', '6'), ('4', '8'), ('4', '9'), ('5', '2'), ('5', '6'), ('5', '7'), ('5', '10'), ('6', '4'), ('6', '8'), ('6', '9'), ('6', '10'), ('7', '6'), ('7', '10'), ('8', '2'), ('8', '3'), ('8', '4'), ('8', '7'), ('8', '10'), ('9', '1'), ('9', '2'), ('9', '3'), ('9', '6'), ('9', '7'), ('9', '10'), ('10', '9')),
(('1', '5'), ('1', '9'), ('1', '10'), ('2', '1'), ('2', '4'), ('2', '6'), ('2', '10'), ('3', '2'), ('3', '6'), ('3', '9'), ('4', '2'), ('4', '3'), ('4', '5'), ('4', '6'), ('5', '3'), ('5', '4'), ('5', '8'), ('5', '10'), ('6', '1'), ('6', '3'), ('6', '9'), ('6', '10'), ('8', '1'), ('8', '3'), ('8', '5'), ('8', '6'), ('9', '1'), ('9', '2'), ('9', '4'), ('9', '5'), ('9', '6'), ('9', '8'), ('10', '1'), ('10', '3'), ('10', '5'), ('10', '6'), ('10', '7'), ('10', '8'), ('10', '9')),
((('james', '5'), ('william', '5'), ('patricia', '10'), ('barbara', '10')), (('sierra', '4'), ('isuzu', '9'), ('chevrolet', '4'), ('ford', '6')), (('p', '4'), ('n', '6'), ('d', '2'), ('s', '6'), ('l', '4'), ('j', '2'))),
(('d', '9'), ('l', '5'), ('isuzu', '5'), ('j', '10')))
problems.append(problem10)
problem11 = (('william', 'robert', 'barbara', 'john', 'patricia', 'james'),
('honda', 'kamaz', 'isuzu', 'ford', 'toyota', 'daewoo'),
('r', 'f', 'q', 'g', 'd', 'p', 'i', 'b', 'e'),
('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'),
(('1', '2'), ('1', '4'), ('1', '5'), ('1', '12'), ('2', '3'), ('2', '7'), ('2', '10'), ('2', '12'), ('2', '15'), ('3', '4'), ('3', '9'), ('4', '6'), ('4', '7'), ('4', '10'), ('4', '14'), ('5', '1'), ('5', '2'), ('5', '4'), ('5', '6'), ('6', '11'), ('6', '13'), ('6', '15'), ('7', '2'), ('7', '10'), ('7', '12'), ('7', '13'), ('7', '15'), ('8', '14'), ('9', '5'), ('9', '12'), ('9', '13'), ('10', '5'), ('10', '6'), ('10', '8'), ('10', '12'), ('10', '13'), ('11', '8'), ('11', '14'), ('12', '1'), ('12', '8'), ('12', '13'), ('13', '3'), ('13', '5'), ('13', '11'), ('14', '1'), ('14', '13'), ('15', '3'), ('15', '9')),
(('1', '5'), ('2', '1'), ('2', '3'), ('2', '7'), ('2', '11'), ('2', '15'), ('3', '1'), ('3', '2'), ('3', '10'), ('3', '14'), ('4', '2'), ('4', '7'), ('5', '2'), ('5', '6'), ('5', '7'), ('5', '10'), ('5', '15'), ('6', '1'), ('6', '3'), ('6', '13'), ('7', '8'), ('8', '3'), ('8', '7'), ('8', '11'), ('9', '4'), ('9', '6'), ('10', '11'), ('11', '3'), ('11', '7'), ('11', '14'), ('11', '15'), ('12', '5'), ('12', '6'), ('12', '8'), ('12', '9'), ('13', '3'), ('13', '5'), ('13', '10'), ('13', '14'), ('13', '15'), ('14', '4'), ('14', '11'), ('15', '1'), ('15', '3'), ('15', '8'), ('15', '9'), ('15', '10'), ('15', '13')),
((('william', '8'), ('robert', '15'), ('barbara', '4'), ('john', '15'), ('patricia', '9'), ('james', '9')), (('honda', '9'), ('kamaz', '9'), ('isuzu', '11'), ('ford', '10'), ('toyota', '5'), ('daewoo', '15')), (('r', '7'), ('f', '13'), ('q', '12'), ('g', '3'), ('d', '12'), ('p', '1'), ('i', '2'), ('b', '9'), ('e', '7'))),
(('honda', '2'), ('f', '11'), ('q', '12'), ('kamaz', '7'), ('g', '10'), ('b', '6')))
# problems.append(problem11)
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
    
    for problem in problems:
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
    # result = check_problem(p, search.breadth_first_graph_search, timeout)
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
    solve_problems(problems)
    
if __name__ == '__main__':
    main()
