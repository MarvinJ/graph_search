from maze import Cell
from maze import Maze
from collections import deque
from copy import deepcopy
import Queue as Q
from collections import defaultdict


class BFS:
    def __init__(self, filename):
        self.curr_maze = Maze(filename)
        self.maze_filename = filename
        self.num_nodes_expand = 0
        visited = set();
        temp_queue = deque()
        temp_queue.append(self.curr_maze.start_cell)
        visited.add(self.curr_maze.start_cell)  # Check visited before pushing

        # a mapping relation between nodes. For backtracking the solution path
        self.parent_dict = {}
        while len(temp_queue) != 0:
            temp_cell = temp_queue.popleft();
            # if the node contains the goal state, return solution
            self.num_nodes_expand += 1  # number of nodes expand
            if temp_cell in self.curr_maze.target_cells:
                print "noob sushi"
                break;
            temp_neighbors = self.curr_maze.get_neighbors(temp_cell.x_coord, temp_cell.y_coord)

            for neighbor in temp_neighbors:
                if neighbor not in visited:
                    temp_queue.append(neighbor)
                    visited.add(neighbor)  # Add to explored set
                    self.parent_dict[(neighbor.x_coord, neighbor.y_coord)] = (temp_cell.x_coord, temp_cell.y_coord)

    ''' return a list of coordinates forming the solution path
    '''

    def get_solution_path(self):
        # get goal cell
        goal_cell_coord = (self.curr_maze.target_cells[0].x_coord, self.curr_maze.target_cells[0].y_coord)
        print "goal cell location: " + str(goal_cell_coord[0]) + "," + str(goal_cell_coord[1])
        solution_path = [goal_cell_coord]
        cell_coord = goal_cell_coord
        test_set = set();
        test_set.add(goal_cell_coord)
        while self.parent_dict.has_key(cell_coord):
            parent_coord = self.parent_dict[cell_coord]
            solution_path.insert(0, parent_coord)
            if parent_coord in test_set:
                print "loop stop me "
            test_set.add(parent_coord)
            cell_coord = parent_coord

        return solution_path

    def print_solution_on_maze(self):
        list_cells = deepcopy(self.curr_maze.list_cell)
        output_file = open('solution_bfs_' + self.maze_filename, 'w')
        solution_path = self.get_solution_path()
        for row in list_cells:
            row_str = ''
            for c in row:
                if c.type == ' ' and (c.x_coord, c.y_coord) in solution_path:
                    row_str += '.'
                else:
                    row_str += c.type
            output_file.write(row_str)
            output_file.write('\n')
        output_file.close()

    def print_report(self):
        output_file = open('report_bfs_' + self.maze_filename, 'w')
        path_cost = len(self.get_solution_path()) - 1
        output_file.write('path_cost: ' + str(path_cost) + '\n')
        output_file.write('# of nodes expand: ' + str(self.num_nodes_expand))
        output_file.close()


class DFS:
    def __init__(self, filename):
        self.curr_maze = Maze(filename)
        self.maze_filename = filename
        self.num_nodes_expand = 0
        visited = set();
        temp_queue = deque()
        temp_queue.append(self.curr_maze.start_cell)

        # a mapping relation between nodes. For backtracking the solution path
        self.parent_dict = {}
        while len(temp_queue) != 0:
            temp_cell = temp_queue.pop();  # pop returns the latest element
            # if the node contains the goal state, return solution

            if temp_cell in self.curr_maze.target_cells:
                break;
            if temp_cell not in visited:
                self.num_nodes_expand += 1  # number of nodes expand
                visited.add(temp_cell)
                temp_neighbors = self.curr_maze.get_neighbors(temp_cell.x_coord, temp_cell.y_coord)
                for neighbor in temp_neighbors:
                    if neighbor not in visited:
                        temp_queue.append(neighbor)
                        self.parent_dict[(neighbor.x_coord, neighbor.y_coord)] = (temp_cell.x_coord, temp_cell.y_coord)
        print "DFS init finish"

    ''' return a list of coordinates forming the solution path
    '''

    def get_solution_path(self):
        # get goal cell
        goal_cell_coord = (self.curr_maze.target_cells[0].x_coord, self.curr_maze.target_cells[0].y_coord)
        print "goal cell location: " + str(goal_cell_coord[0]) + "," + str(goal_cell_coord[1])
        solution_path = [goal_cell_coord]
        cell_coord = goal_cell_coord
        test_set = set();
        test_set.add(goal_cell_coord)
        while self.parent_dict.has_key(cell_coord):
            parent_coord = self.parent_dict[cell_coord]
            solution_path.insert(0, parent_coord)
            print "parent coord is "
            print parent_coord
            print "cell coord is"
            print cell_coord
            if parent_coord in test_set:
                print "parent coord is "
                print parent_coord
                print "cell coord is"
                print cell_coord
                print "loop stop me "
                break
            test_set.add(parent_coord)
            cell_coord = parent_coord

        return solution_path

    def print_solution_on_maze(self):
        list_cells = self.curr_maze.list_cell
        output_file = open('solution_dfs_' + self.maze_filename, 'w')
        solution_path = self.get_solution_path()
        print len(list_cells)
        for row in list_cells:
            row_str = ''
            for c in row:
                if c.type == ' ' and (c.x_coord, c.y_coord) in solution_path:
                    row_str += '.'
                else:
                    row_str += c.type
            output_file.write(row_str)
            output_file.write('\n')
        output_file.close()

    def print_report(self):
        output_file = open('report_dfs_' + self.maze_filename, 'w')
        path_cost = len(self.get_solution_path()) - 1
        output_file.write('path_cost: ' + str(path_cost) + '\n')
        output_file.write('# of nodes expand: ' + str(self.num_nodes_expand))
        output_file.close()


class Greedy:
    def __init__(self, filename):
        self.curr_maze = Maze(filename)
        self.maze_filename = filename
        self.num_nodes_expand = 0

        visited = set();
        goal_cell = self.curr_maze.target_cells[0]
        temp_queue = Q.PriorityQueue()

        temp_queue.put((self.heuristic(self.curr_maze.start_cell, goal_cell), self.curr_maze.start_cell))
        visited.add(self.curr_maze.start_cell)  # Check visited before pushing

        # a mapping relation between nodes. For backtracking the solution path
        self.parent_dict = {}
        while not temp_queue.empty():
            temp_cell = temp_queue.get()[1];
            # if the node contains the goal state, return solution
            self.num_nodes_expand += 1  # number of nodes expand
            if temp_cell in self.curr_maze.target_cells:
                print "noob sushi"
                break;
            temp_neighbors = self.curr_maze.get_neighbors(temp_cell.x_coord, temp_cell.y_coord)

            for neighbor in temp_neighbors:
                if neighbor not in visited:
                    temp_queue.put((self.heuristic(neighbor, goal_cell), neighbor))
                    visited.add(neighbor)  # Add to explored set
                    self.parent_dict[(neighbor.x_coord, neighbor.y_coord)] = (temp_cell.x_coord, temp_cell.y_coord)

    ''' return a list of coordinates forming the solution path
    '''

    def get_solution_path(self):
        # get goal cell
        goal_cell_coord = (self.curr_maze.target_cells[0].x_coord, self.curr_maze.target_cells[0].y_coord)
        print "goal cell location: " + str(goal_cell_coord[0]) + "," + str(goal_cell_coord[1])
        solution_path = [goal_cell_coord]
        cell_coord = goal_cell_coord
        test_set = set();
        test_set.add(goal_cell_coord)
        while self.parent_dict.has_key(cell_coord):
            parent_coord = self.parent_dict[cell_coord]
            solution_path.insert(0, parent_coord)
            if parent_coord in test_set:
                print "loop stop me "
            test_set.add(parent_coord)
            cell_coord = parent_coord

        return solution_path

    def print_solution_on_maze(self):
        list_cells = deepcopy(self.curr_maze.list_cell)
        output_file = open('solution_greedy_' + self.maze_filename, 'w')
        solution_path = self.get_solution_path()
        for row in list_cells:
            row_str = ''
            for c in row:
                if c.type == ' ' and (c.x_coord, c.y_coord) in solution_path:
                    row_str += '.'
                else:
                    row_str += c.type
            output_file.write(row_str)
            output_file.write('\n')
        output_file.close()

    def print_report(self):
        output_file = open('report_greedy_' + self.maze_filename, 'w')
        path_cost = len(self.get_solution_path()) - 1
        output_file.write('path_cost: ' + str(path_cost) + '\n')
        output_file.write('# of nodes expand: ' + str(self.num_nodes_expand))
        output_file.close()

    # given two cell objects, find manhatan dist
    def heuristic(self, cell1, cell2):
        return abs(cell1.x_coord - cell2.x_coord) + abs(cell1.y_coord - cell2.y_coord)



class AStar:
    def __init__(self, filename):
        self.curr_maze = Maze(filename)
        self.maze_filename = filename
        self.num_nodes_expand = 0
        self.parent_dict = {}
        closed_set = set(); #  a set of visited nodes
        open_set = set(); #  function like a priority queue
        parent_dict = {}
        start_cell = self.curr_maze.start_cell
        goal_cell = self.curr_maze.target_cells[0]

        open_set.add(start_cell)
        g_score = defaultdict(lambda: float('+inf'))
        f_score = defaultdict(lambda: float('+inf'))

        g_score[start_cell] = 0
        f_score[start_cell] = self.heuristic(start_cell, goal_cell)
        while open_set:
            current_cell = min(open_set, key=lambda c: f_score[c])

            if current_cell == goal_cell:
                break

            open_set.remove(current_cell)
            self.num_nodes_expand += 1
            closed_set.add(current_cell)
            for neighbor in self.curr_maze.get_neighbors(current_cell.x_coord, current_cell.y_coord):

                if neighbor in closed_set: #  check if it has been visited
                    continue
                temp_g_score = g_score.get(current_cell) + 1
                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif temp_g_score >= g_score[neighbor]:
                    continue #  not a better path

                self.parent_dict[(neighbor.x_coord, neighbor.y_coord)] = (current_cell.x_coord, current_cell.y_coord)
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal_cell)


    ''' return a list of coordinates forming the solution path
    '''

    def get_solution_path(self):
        # get goal cell
        goal_cell_coord = (self.curr_maze.target_cells[0].x_coord, self.curr_maze.target_cells[0].y_coord)
        print "goal cell location: " + str(goal_cell_coord[0]) + "," + str(goal_cell_coord[1])
        solution_path = [goal_cell_coord]
        cell_coord = goal_cell_coord
        test_set = set();
        test_set.add(goal_cell_coord)
        while self.parent_dict.has_key(cell_coord):
            parent_coord = self.parent_dict[cell_coord]
            solution_path.insert(0, parent_coord)
            if parent_coord in test_set:
                print "loop stop me "
            test_set.add(parent_coord)
            cell_coord = parent_coord

        return solution_path

    def print_solution_on_maze(self):
        list_cells = deepcopy(self.curr_maze.list_cell)
        output_file = open('solution_AStar_' + self.maze_filename, 'w')
        solution_path = self.get_solution_path()
        for row in list_cells:
            row_str = ''
            for c in row:
                if c.type == ' ' and (c.x_coord, c.y_coord) in solution_path:
                    row_str += '.'
                else:
                    row_str += c.type
            output_file.write(row_str)
            output_file.write('\n')
        output_file.close()

    def print_report(self):
        output_file = open('report_AStar_' + self.maze_filename, 'w')
        path_cost = len(self.get_solution_path()) - 1
        output_file.write('path_cost: ' + str(path_cost) + '\n')
        output_file.write('# of nodes expand: ' + str(self.num_nodes_expand))
        output_file.close()

    # given two cell objects, find manhatan dist
    def heuristic(self, cell1, cell2):
        return abs(cell1.x_coord - cell2.x_coord) + abs(cell1.y_coord - cell2.y_coord)


# part 1.2 eating many dots at the same time

class AdvancedAstar:
    def __init__(self, filename):
        self.curr_maze = Maze(filename)
        self.maze_filename = filename
        self.num_nodes_expand = 0
        self.list_goals = self.curr_maze.target_cells
        current_cell = self.curr_maze.start_cell
        self.parent_dicts = {}
        self.step_dict = {}
        #print "hello world"
        self.step = 0
        while len(self.list_goals)!=0:
            closed_set = set()  # a set of visited nodes
            open_set = set() # function like a priority queue
            open_set.add(current_cell)
            goal_cell = self.next_goal(current_cell)[0]
            #print 'goal cell is ' + str(goal_cell.x_coord) + str(goal_cell.y_coord)
            #print "I am here"
            g_score = defaultdict(lambda: float('+inf'))
            f_score = defaultdict(lambda: float('+inf'))
            # g_score and f_score is the dictionary to store the heuristic function here
            g_score[current_cell] = 0
            f_score[current_cell] = self.next_goal(current_cell)[1]
            parent_dict = {}
            while open_set:
                #print "I am there"
                current_cell = min(open_set, key=lambda c: f_score[c])
                if current_cell == goal_cell:
                   ## print "begin remove"
                    print "current cell is " + str(current_cell.x_coord) + str(current_cell.y_coord)
                    self.step+=1
                    self.list_goals.remove(goal_cell)

                    if self.step<=9:
                        print "noob"
                        self.step_dict[current_cell] = str(self.step)
                    elif self.step>9 and self.step<=35:
                        print "shit"
                        self.step_dict[current_cell] =chr(ord('a')+self.step-10)
                    elif self.step>35 and self.step<=61:
                        print "idiot"
                        self.step_dict[current_cell] = chr(ord('A') + self.step-36 )
                    else:
                        pass
                    break
                #print "continue"
                open_set.remove(current_cell)
                # check if we pass one of the goals or not
                if current_cell in self.list_goals:
                    #print "pass goals"
                    print "current cell is " + str(current_cell.x_coord) + str(current_cell.y_coord)
                    self.list_goals.remove(current_cell)
                    self.step +=1
                    if self.step<=9:
                        print "hello i am qi"
                        self.step_dict[current_cell] = str(self.step)
                    elif self.step>9 and self.step<=35:
                        print "hello i am marvin"
                        self.step_dict[current_cell] =chr(ord('a')+self.step-10)
                    elif self.step>35 and self.step<=61:
                        print "hello i am sushi"
                        self.step_dict[current_cell] = chr(ord('A') + self.step-36 )
                    else:
                        pass


                self.num_nodes_expand += 1
                closed_set.add(current_cell)
                #print "begin neighbor"
                for neighbor in self.curr_maze.get_neighbors(current_cell.x_coord, current_cell.y_coord):
                    #print "check neighbor"
                    if neighbor in closed_set:  # check if it has been visited
                        continue
                    temp_g_score = g_score.get(current_cell) + 1
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                    elif temp_g_score >= g_score[neighbor]:
                        continue  # not a better path

                    parent_dict[(neighbor.x_coord, neighbor.y_coord)] = (
                    current_cell.x_coord, current_cell.y_coord)
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal_cell)

            # at the end of while loop current cell already equals to goal_cell
            self.parent_dicts[goal_cell] = parent_dict

    def get_solution_path(self):
        # get goal cell
        # iterate each goal and paths to the goal
        solution_paths = []
        for k in self.parent_dicts:
            #print "get each path"
            goal_cell_coord = (k.x_coord, k.y_coord)
            #goal_cell_coord = (self.curr_maze.target_cells[0].x_coord, self.curr_maze.target_cells[0].y_coord)
            #print "goal cell location: " + str(goal_cell_coord[0]) + "," + str(goal_cell_coord[1])
            solution_path = [goal_cell_coord]
            cell_coord = goal_cell_coord
            test_set = set();
            test_set.add(goal_cell_coord)
            while self.parent_dicts[k].has_key(cell_coord):
                #print " in path"
                parent_coord = self.parent_dicts[k][cell_coord]
                solution_path.insert(0, parent_coord)
                if parent_coord in test_set:
                    print "loop stop me "
                test_set.add(parent_coord)
                cell_coord = parent_coord
            solution_paths.append(solution_path)
        return solution_paths

    def print_solution_on_maze(self):
        #print "here we go"
        list_cells =self.curr_maze.list_cell
        print 'dict is' + str(len(self.step_dict)) + 'length'
        for i in self.step_dict:
            print i
            print 'coordinate is' + str(i.x_coord) + str(i.y_coord)
        output_file = open('solution_Advanced_AStar_' + self.maze_filename, 'w')
        solution_paths = self.get_solution_path()
        for row in list_cells:
            row_str = ''
            for c in row:
                #print c.x_coord
                #print c.y_coord
                #print "iteration"
                print c
                if self.step_dict.has_key(c):
                    print "step counts"
                    row_str += self.step_dict[c]
                    print "step count is " + self.step_dict[c]
                else:
                    print "here we are"
                    row_str += c.type
            output_file.write(row_str)
            output_file.write('\n')
        output_file.close()
        # write the file when we are done with each row


    def print_report(self):
        output_file = open('report_Advanced_AStar_' + self.maze_filename, 'w')
        path_cost = 0
        for temp_path in self.get_solution_path():
            path_cost += len(temp_path)-1
        output_file.write('path_cost: ' + str(path_cost) + '\n')
        output_file.write('# of nodes expand: ' + str(self.num_nodes_expand))
        output_file.close()



    def next_goal(self, current_cell):
        temp_dist = float('+inf')
        result_goal = None
        for temp_goal in self.list_goals:
            int_x = temp_goal.x_coord
            int_y = temp_goal.y_coord
            if (abs(int_x- current_cell.x_coord) + abs(int_y - current_cell.y_coord))< temp_dist:
                temp_dist = abs(int_x- current_cell.x_coord) + abs(int_y- current_cell.y_coord)
                result_goal = temp_goal
        #print "result goal is " + result_goal.x_coord + result_goal.y_coord
        return (result_goal, abs(int_x-current_cell.x_coord)+ abs(int_y - current_cell.y_coord))


    def heuristic(self, cell1, cell2):
        return abs(cell1.x_coord - cell2.x_coord) + abs(cell1.y_coord - cell2.y_coord)

# improve the function here
# extra credit here
'''
class old_Astar_Advanced:
    def __init__(self, filename):
        self.curr_maze = Maze(filename)
        self.maze_filename = filename
        self.num_nodes_expand = 0
        self.list_goals = self.curr_maze.target_cells
        # dictionary to store the starting state, ending state and the nodes pass
        self.pass_dict = {}
        #print "hello world"
        self.parent_dict = {}
        while len(self.list_goals)!=0:
            current_cell = self.curr_maze.start_cell
            closed_set = set()  # a set of visited nodes
            open_set = set() # function like a priority queue
            open_set.add(current_cell)
            goal_cell = self.list_goals[0]
            pass_cell = []
            print 'goal cell is ' + str(goal_cell.x_coord) + str(goal_cell.y_coord)
            #print "I am here"
            g_score = defaultdict(lambda: float('+inf'))
            f_score = defaultdict(lambda: float('+inf'))
            # g_score and f_score is the dictionary to store the heuristic function here
            g_score[current_cell] = 0
            f_score[current_cell] = self.next_goal(current_cell)[1]
            parent_dict = {}
            while open_set:
                #print "I am there"
                current_cell = min(open_set, key=lambda c: f_score[c])
                if current_cell == goal_cell:
                   # print "begin remove"
                    if goal_cell in self.list_goals:
                        #print "remove"
                        self.list_goals.remove(goal_cell)
                    break;
                #print "continue"
                open_set.remove(current_cell)
                # check if the current cell is one of the goals or not
                if current_cell in self.list_goals:
                    print "pass goals"
                    pass_cell.append(current_cell)
                self.num_nodes_expand += 1
                closed_set.add(current_cell)
                #print "begin neighbor"
                for neighbor in self.curr_maze.get_neighbors(current_cell.x_coord, current_cell.y_coord):
                    #print "check neighbor"
                    if neighbor in closed_set:  # check if it has been visited
                        continue
                    temp_g_score = g_score.get(current_cell) + 1
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                    elif temp_g_score >= g_score[neighbor]:
                        continue  # not a better path

                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal_cell)


            # at the end of while loop current cell already equals to goal_cell
            self.pass_dict[goal_cell] = pass_cell

    def _extra_credit(self):
        # perform after the hashmap is done
        # make sure there is no other goal is on the way
        self.parent_dicts = {}
        # dictionary to store the starting state, ending state and the nodes pass
        self.pass_dict = {}
        self.num_nodes_expand = 0
        current_cell = self.curr_maze.start_cell
        self.parent_dicts = {}
        while len(self.pass_dict)!=0:
            closed_set = set()  # a set of visited nodes
            open_set = set()  # function like a priority queue
            open_set.add(current_cell)
            parent_dict = {}
            for k in self.pass_dict:
                # case of current goal
                # which means no other goals on the path
                if len(self.pass_dict[k])==0:
                    goal_cell = k
                    g_score = defaultdict(lambda: float('+inf'))
                    f_score = defaultdict(lambda: float('+inf'))
                    # g_score and f_score is the dictionary to store the heuristic function here
                    g_score[current_cell] = 0
                    f_score[current_cell] = self.next_goal(current_cell)[1]
                    while open_set:
                        # print "I am there"
                        current_cell = min(open_set, key=lambda c: f_score[c])
                        if current_cell == goal_cell:
                            # print "begin remove"
                            # remove the goal cell in the lists of other entries
                            break
                        # print "continue"
                        open_set.remove(current_cell)
                        for neighbor in self.curr_maze.get_neighbors(current_cell.x_coord, current_cell.y_coord):
                            # print "check neighbor"
                            if neighbor in closed_set:  # check if it has been visited
                                continue
                            temp_g_score = g_score.get(current_cell) + 1
                            if neighbor not in open_set:
                                open_set.add(neighbor)
                            elif temp_g_score >= g_score[neighbor]:
                                continue  # not a better path

                            g_score[neighbor] = temp_g_score
                            f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal_cell)
                            parent_dict[(neighbor.x_coord, neighbor.y_coord)] = (
                                current_cell.x_coord, current_cell.y_coord)
                    self.parent_dicts[goal_cell] = parent_dict

    def get_solution_path(self):
        # get goal cell
        # iterate each goal and paths to the goal
        solution_paths = []
        for k in self.parent_dicts:
            #print "get each path"
            goal_cell_coord = (k.x_coord, k.y_coord)
            #goal_cell_coord = (self.curr_maze.target_cells[0].x_coord, self.curr_maze.target_cells[0].y_coord)
            print "goal cell location: " + str(goal_cell_coord[0]) + "," + str(goal_cell_coord[1])
            solution_path = [goal_cell_coord]
            cell_coord = goal_cell_coord
            test_set = set();
            test_set.add(goal_cell_coord)
            while self.parent_dicts[k].has_key(cell_coord):
                #print " in path"
                parent_coord = self.parent_dicts[k][cell_coord]
                solution_path.insert(0, parent_coord)
                if parent_coord in test_set:
                    print "loop stop me "
                test_set.add(parent_coord)
                cell_coord = parent_coord
            solution_paths.append(solution_path)
        return solution_paths

    def print_solution_on_maze(self):
        list_cells = deepcopy(self.curr_maze.list_cell)
        output_file = open('solution_Advanced_AStar_' + self.maze_filename, 'w')
        solution_paths = self.get_solution_path()
        for i in range(len(solution_paths)):
            solution_path = solution_paths[i]
            for row in list_cells:
                row_str = ''
                for c in row:
                    if c.type == ' ' and (c.x_coord, c.y_coord) in solution_path:
                        row_str += '.'
                    else:
                        row_str += c.type
                output_file.write(row_str)
                output_file.write('\n')
        output_file.close()

    def print_report(self):
        output_file = open('report_Advanced_AStar_' + self.maze_filename, 'w')
        path_cost = 0
        for temp_path in self.get_solution_path():
            path_cost += len(temp_path)-1
        output_file.write('path_cost: ' + str(path_cost) + '\n')
        output_file.write('# of nodes expand: ' + str(self.num_nodes_expand))
        output_file.close()



    def next_goal(self, current_cell):
        temp_dist = float('+inf')
        result_goal = None
        for temp_goal in self.list_goals:
            int_x = temp_goal.x_coord
            int_y = temp_goal.y_coord
            if (abs(int_x- current_cell.x_coord) + abs(int_y - current_cell.y_coord))< temp_dist:
                temp_dist = abs(int_x- current_cell.x_coord) + abs(int_y- current_cell.y_coord)
                result_goal = temp_goal
        #print "result goal is " + result_goal.x_coord + result_goal.y_coord
        return (result_goal, abs(int_x-current_cell.x_coord)+ abs(int_y - current_cell.y_coord))


    def heuristic(self, cell1, cell2):
        return abs(cell1.x_coord - cell2.x_coord) + abs(cell1.y_coord - cell2.y_coord)

'''

test_bfs = AdvancedAstar('bigDots.txt')
print "entering print sol on maze"
test_bfs.print_solution_on_maze()
print "entering print report"
#test_bfs.print_report()
test_bfs.print_report()