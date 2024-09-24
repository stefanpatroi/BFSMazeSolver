from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict
from queue import Queue

class MazeVisitor(ABC):
    @abstractmethod
    def visit(self, maze):
        pass
class Turn(Enum):
    RIGHT = 1
    LEFT = 2
    NONE = 3
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    def turn_right(self):
        if self == Direction.UP:
            return Direction.RIGHT
        elif self == Direction.DOWN:
            return Direction.LEFT
        elif self == Direction.LEFT:
            return Direction.UP
        elif self == Direction.RIGHT:
            return Direction.DOWN
        raise ValueError(f"Unexpected value: {self}")

    def turn_left(self):
        if self == Direction.UP:
            return Direction.LEFT
        elif self == Direction.DOWN:
            return Direction.RIGHT
        elif self == Direction.LEFT:
            return Direction.DOWN
        elif self == Direction.RIGHT:
            return Direction.UP
        raise ValueError(f"Unexpected value: {self}")

    def spin(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.LEFT
        raise ValueError(f"Unexpected value: {self}")

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def move(self, direction):
        if direction == Direction.UP:
            return self.add(Position(0, -1))
        elif direction == Direction.DOWN:
            return self.add(Position(0, 1))
        elif direction == Direction.LEFT:
            return self.add(Position(-1, 0))
        elif direction == Direction.RIGHT:
            return self.add(Position(1, 0))
        raise ValueError(f"Unexpected direction: {direction}")
    
    def __str__(self):
        return f"Position({self.x},{self.y})"

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

class Maze:
    def __init__(self, file_path):
        print(f"Reading the maze from file {file_path}")
        with open(file_path, 'r') as reader:
            lines = [line.rstrip() for line in reader]  

        height = len(lines)
        width = max(len(line) for line in lines)

        self.maze = [[False for _ in range(width)] for _ in range(height)]

        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == '#':
                    self.maze[i][j] = True  
                elif char == ' ':
                    self.maze[i][j] = False  

        self.start = self.find_start()
        self.end = self.find_end()

    def find_start(self):
        for i in range(len(self.maze)):
            if not self.maze[i][0]:  
                print(f"Start Pos: {Position(0, i)}")
                return Position(0, i)
        raise Exception("Invalid maze (no start position available)")

    def find_end(self):
        for i in range(len(self.maze)):
            if not self.maze[i][-1]:  
                print(f"End Pos: {Position(len(self.maze[0]) - 1, i)}")
                return Position(len(self.maze[0]) - 1, i)
        raise Exception("Invalid maze (no end position available)")

    def is_wall(self, pos):
        if 0 <= pos.y < len(self.maze) and 0 <= pos.x < len(self.maze[0]):
            return self.maze[pos.y][pos.x]
        else:
            return True  

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_size_x(self):
        return len(self.maze[0])

    def get_size_y(self):
        return len(self.maze)
    def validate_path(self, path):
        r2l = (self.validate_path_dir(path, self.get_start(), Direction.RIGHT, self.get_end()))
               
        l2r = (self.validate_path_dir(path, self.get_end(), Direction.LEFT, self.get_start()))
        return (r2l or l2r)

    def validate_path_dir(self, path, start_pos, start_dir, end_pos):
        pos = start_pos
        dir = start_dir
    
        for c in path.get_path_steps():
            if c == 'F':
                pos = pos.move(dir)
                if self.is_wall(pos) or not (0 <= pos.x < self.get_size_x() and 0 <= pos.y < self.get_size_y()):
                    return False
            elif c == 'R':
                dir = dir.turn_right()
            elif c == 'L':
                dir = dir.turn_left()
        
            print(f"Current Position: {pos}")
            print(f"Current Direction: {dir}")
        return pos == end_pos
    
    def print_maze(self):
        for row in self.maze:
            for cell in row:
                if cell:
                    print('#', end='') 
                else:
                    print(' ', end='')  
            print() 
    
    def accept(self, visitor):
        visitor.visit(self)

class Path:
    def __init__(self, path_string=None):
        self.path = []
        if path_string:
            self.expand_factorized_string_path(path_string)

    def expand_factorized_string_path(self, path):
        i = 0
        while i < len(path):
            if not path[i].isdigit():
                self.add_step(path[i])
                i += 1
            else:
                count = 0
                while i < len(path) and path[i].isdigit():
                    count = count * 10 + int(path[i])
                    i += 1
                if i < len(path):
                    step = path[i] * count  
                    for char in step:
                        self.add_step(char)
                    i += 1
    def get_factorized_form(self):
        if not self.path:
            return ''
        
        sb = []
        i = 0
        while i < len(self.path):
            current = self.path[i]
            count = 0
            
            while i < len(self.path) and self.path[i] == current:
                count += 1
                i += 1
            
            if count == 1:
                sb.append(current)
            else:
                sb.append(str(count))
                sb.append(current)
        
        return Path(''.join(sb))
    
    def add_step(self, step):
        if step not in {'F', 'L', 'R'}:
            raise ValueError(f"Instruction '{step}' is invalid. Must be 'F', 'L', or 'R'.")
        self.path.append(step)

    def get_path_steps(self):
        return list(self.path)
    
    def __str__(self):
        return ''.join(self.path)
    def reverse_order(self):
        reversed_path = []
        for current in reversed(self.path):
            if current == 'R':
                reversed_path.append('L')
            elif current == 'L':
                reversed_path.append('R')
            else:
                reversed_path.append(current)
        return Path(''.join(reversed_path))

class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze: Maze) -> Path:
        pass 

class RightHandSolver(MazeSolver):

    def solve(self, maze):
        path = Path()  
        current_pos = maze.get_start()
        direction = Direction.RIGHT 

        while current_pos != maze.get_end():
            if not maze.is_wall(current_pos.move(direction.turn_right())):
                direction = direction.turn_right()
                path.add_step('R')
                current_pos = current_pos.move(direction)
                path.add_step('F')
            else:
                if not maze.is_wall(current_pos.move(direction)):
                    current_pos = current_pos.move(direction)
                    path.add_step('F')
                elif not maze.is_wall(current_pos.move(direction.turn_left())):
                    direction = direction.turn_left()
                    path.add_step('L')
                    current_pos = current_pos.move(direction)
                    path.add_step('F')
                else:
                    direction = direction.spin()
                    path.add_step('R')
                    path.add_step('R')

            print(f"Current Position: {current_pos} \n")

        print(f"Path: {path.get_factorized_form()}")
        return path
    
class AdjacencyListBuilder(MazeVisitor):
    def __init__(self):
        self.adjacency_list = defaultdict(list)

    def visit(self, maze: Maze):
        size_x = maze.get_size_x()
        size_y = maze.get_size_y()

        for y in range(size_y):
            for x in range(size_x):
                curr_pos = Position(x, y)

                if not maze.is_wall(curr_pos):
                    adjacent_walkable_positions = []
                    
                    if x > 0 and not maze.is_wall(Position(x - 1, y)):
                        adjacent_walkable_positions.append(Position(x - 1, y))
                    if x < size_x - 1 and not maze.is_wall(Position(x + 1, y)):
                        adjacent_walkable_positions.append(Position(x + 1, y))
                    if y > 0 and not maze.is_wall(Position(x, y - 1)):
                        adjacent_walkable_positions.append(Position(x, y - 1))
                    if y < size_y - 1 and not maze.is_wall(Position(x, y + 1)):
                        adjacent_walkable_positions.append(Position(x, y + 1))

                    self.adjacency_list[curr_pos] = adjacent_walkable_positions

    def get_adjacency_list(self):
        return self.adjacency_list

    def print_adjacency_list(self):
        for current_position, adjacent_positions in self.adjacency_list.items():
            print(f"Adjacent positions for position {current_position}: ", end="")
            if not adjacent_positions:
                print("None")
            else:
                print(" ".join(str(adjacent_position) for adjacent_position in adjacent_positions))

class GraphSolver(MazeSolver):

    def solve(self, maze):
        path = Path()

        adjacency_list_builder = AdjacencyListBuilder()
        maze.accept(adjacency_list_builder)
        adj_list = adjacency_list_builder.get_adjacency_list()

        start = maze.get_start()
        end = maze.get_end()

        node_path = {}
        to_visit = Queue()
        visited = set()

        to_visit.put(start)
        visited.add(start)

        while not to_visit.empty():
            curr = to_visit.get()

            if curr == end:
                path = self.generate_path(node_path, start, end)
                break

            for touching in adj_list.get(curr, []):
                if touching not in visited:
                    visited.add(touching)
                    to_visit.put(touching)
                    node_path[touching] = curr

        return path

    def generate_path(self, node_path, start_node, end_node):
        path = Path()
        curr_node = end_node
        dir = Direction.LEFT

        while curr_node != start_node:
            prev_node = node_path[curr_node]
            want_dir = self.position_orientation(curr_node, prev_node)
            want_turn = self.turn_choice(dir, want_dir)

            if want_turn == Turn.LEFT:
                path.add_step('L')
            elif want_turn == Turn.RIGHT:
                path.add_step('R')

            dir = want_dir
            curr_node = prev_node
            path.add_step('F')

        return path

    def position_orientation(self, first, second):
        first_x, first_y = first.x, first.y
        second_x, second_y = second.x, second.y

        if first_x == second_x:
            if first_y > second_y:
                return Direction.UP
            else:
                return Direction.DOWN
        else:
            if first_x > second_x:
                return Direction.LEFT
            else:
                return Direction.RIGHT

    def turn_choice(self, current, wanted_dir):
        if current == Direction.RIGHT:
            if wanted_dir == Direction.UP:
                return Turn.LEFT
            elif wanted_dir == Direction.DOWN:
                return Turn.RIGHT
            else:
                return Turn.NONE
        elif current == Direction.LEFT:
            if wanted_dir == Direction.UP:
                return Turn.RIGHT
            elif wanted_dir == Direction.DOWN:
                return Turn.LEFT
            else:
                return Turn.NONE
        elif current == Direction.UP:
            if wanted_dir == Direction.LEFT:
                return Turn.LEFT
            elif wanted_dir == Direction.RIGHT:
                return Turn.RIGHT
            else:
                return Turn.NONE
        else:  
            if wanted_dir == Direction.LEFT:
                return Turn.RIGHT
            elif wanted_dir == Direction.RIGHT:
                return Turn.LEFT
            else:
                return Turn.NONE


def main():
    print("** Starting Maze Runner")

    file_path = input("Enter the file path of the maze: ")

    try:
        maze = Maze(file_path)
        maze.print_maze()

        validate_path = input("Do you want to validate a path? (yes/no): ").strip().lower()
        if validate_path == 'yes':
            path_input = input("Enter the path to be validated: ")
            path = Path(path_input)
            if maze.validate_path(path):
                print("Correct path")
            else:
                print("Incorrect path")
        else:
            method = input("Enter the solving method (righthand/graph): ").strip().lower()
            solver = None
            if method == "righthand":
                print("RightHand algorithm chosen.")
                solver = RightHandSolver()
                path = solver.solve(maze) 
                l2r_path_f = path.get_factorized_form()
                r2l_path_f = path.reverse_order().get_factorized_form()
                print(f"Right to Left Solution: {r2l_path_f}")
                print(f"Left to Right Solution: {l2r_path_f}")
            elif method == "graph":
                print("Graph algorithm chosen.")
                solver = GraphSolver()
                path2 = solver.solve(maze)
                r2l = path2.get_factorized_form()
                l2r = path2.reverse_order().get_factorized_form()
                print(f"Right to Left Solution: {r2l}")
                print(f"Left to Right Solution: {l2r}")
            else:
                print(f"Method '{method}' not supported.")
                return
        
    except Exception as e:
        print(f"MazeSolver failed. Reason: {e}")

    print("End of MazeRunner")


main()