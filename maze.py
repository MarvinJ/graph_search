# class for the node in the maze
import os


class Cell:
    def __init__(self, x_coord, y_coord, type):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.type = type


class Maze:

    # read file into a maze and create a maze according to the file
    def __init__(self, file_name):
        dir_path = os.path.dirname(os.path.realpath(file_name))
        file_path = dir_path + '/' + file_name
        self.list_cell = []
        self.target_cells = []
        with open(file_path) as f:
            row = 0
            for line in f:
                col = 0
                temp_list = []
                for cell in line:
                    if cell in [' ', '.', 'P', '%']:
                        temp_cell = Cell(row, col, cell);
                        if cell=='.':
                            self.target_cells.append(temp_cell)
                        if cell=='P':
                            self.start_cell = temp_cell
                        temp_list.append(temp_cell)
                    col += 1
                row += 1
                self.list_cell.append(temp_list)

                # return a cell at specific coordinate
    def return_cell(self, row, col):
        return self.list_cell[row][col]


    def get_neighbors(self, row, col):
        result_cell = []
        if self.valid(row, col-1) and self.list_cell[row][col-1].type!='%':
            result_cell.append(self.list_cell[row][col-1])
        if self.valid(row,col+1) and self.list_cell[row][col+1].type!='%':
            result_cell.append(self.list_cell[row][col+1])
        if self.valid(row-1, col) and self.list_cell[row-1][col].type!='%':
            result_cell.append(self.list_cell[row-1][col])
        if self.valid(row+1, col) and self.list_cell[row+1][col].type!='%':
            result_cell.append(self.list_cell[row+1][col])
        return result_cell


    def valid(self, row, col):
        if row<0 or  row>=len(self.list_cell) or  col<0 or col>=len(self.list_cell[0]):
            return False
        else:
            return True

if __name__ =='__main__':

    test_maze = Maze('mediumMaze.txt')
    print test_maze.start_cell.x_coord
    print test_maze.start_cell.y_coord
    print test_maze.target_cells[0].x_coord
    print test_maze.target_cells[0].y_coord
    print "_________________________________________________________________________________________"
    print len(test_maze.list_cell)
    print (test_maze.list_cell)
    print test_maze.valid(21,41)
    test_cell = test_maze.get_neighbors(2,1)
    for i in test_cell:
        print i.type + 'm'
