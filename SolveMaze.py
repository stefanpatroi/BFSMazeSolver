from abc import ABC, abstractmethod
from enum import Enum

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

class MazeSolver(ABC):

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

class GraphSolver(MazeSolver):


def main():

main()