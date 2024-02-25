import random
import os

class RabbitGame:
    def __init__(self, width, height, num_carrots, num_holes):
        self.width = width
        self.height = height
        self.num_carrots = num_carrots
        self.num_holes = num_holes
        self.grid = [['-' for _ in range(width)] for _ in range(height)]
        self.rabbit_position = None
        self.carrots = set()
        self.rabbit_holes = set()
        self.rabbit_hold_carrot = False

    def generate_map(self):
        # Place rabbit
        self.rabbit_position = (random.randint(0, self.width-1), random.randint(0, self.height-1))
        self.grid[self.rabbit_position[1]][self.rabbit_position[0]] = 'r'

        # Place carrots
        self.carrots = set()
        while len(self.carrots) < self.num_carrots:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if (x, y) != self.rabbit_position:
                self.carrots.add((x, y))
                self.grid[y][x] = 'c'

        # Place rabbit holes
        self.rabbit_holes = set()
        while len(self.rabbit_holes) < self.num_holes:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if (x, y) != self.rabbit_position and (x, y) not in self.carrots:
                self.rabbit_holes.add((x, y))
                self.grid[y][x] = 'O'

    def print_map(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.grid:
            print(" ".join(row))
        print()

        x, y = self.rabbit_position
        rabbit_symbol = 'R' if self.rabbit_hold_carrot else 'r'
        print(f"Rabbit Position: ({x}, {y}), Rabbit Status: {rabbit_symbol}{' (Holding Carrot)' if self.rabbit_hold_carrot else ''}\n")

    def move_rabbit(self, direction):
        x, y = self.rabbit_position
        if direction == 'a' and x > 0:
            x -= 1
        elif direction == 'd' and x < self.width - 1:
            x += 1
        elif direction == 'w' and y > 0:
            y -= 1
        elif direction == 's' and y < self.height - 1:
            y += 1
        elif direction == 'aw' and x > 0 and y > 0:
            x -= 1
            y -= 1
        elif direction == 'as' and x > 0 and y < self.height - 1:
            x -= 1
            y += 1
        elif direction == 'dw' and x < self.width - 1 and y > 0:
            x += 1
            y -= 1
        elif direction == 'ds' and x < self.width - 1 and y < self.height - 1:
            x += 1
            y += 1

        if (x, y) not in self.carrots and (x, y) not in self.rabbit_holes:
            self.grid[self.rabbit_position[1]][self.rabbit_position[0]] = '-'
            self.rabbit_position = (x, y)
            self.grid[y][x] = 'R' if self.rabbit_hold_carrot else 'r'

    def pick_carrot(self):
        if self.rabbit_position in self.carrots and not self.rabbit_hold_carrot:
            self.carrots.remove(self.rabbit_position)
            self.rabbit_hold_carrot = True
            self.grid[self.rabbit_position[1]][self.rabbit_position[0]] = 'R'

    def jump_rabbit(self):
        if self.rabbit_position in self.rabbit_holes:
            x, y = self.rabbit_position
            hole = self.rabbit_holes.difference({(x, y)}).pop()
            self.rabbit_position = hole

    def deposit_carrot(self):
        if self.rabbit_hold_carrot and self.rabbit_position in self.rabbit_holes:
            self.rabbit_hold_carrot = False
            self.carrots -= {self.rabbit_position}
            self.grid[self.rabbit_position[1]][self.rabbit_position[0]] = 'O'

    def is_game_over(self):
        return any(self.rabbit_position in target for target in [self.rabbit_holes, self.carrots])


def play_game():
    width = int(input("Enter the width of the map: "))
    height = int(input("Enter the height of the map: "))
    num_carrots = int(input("Enter the number of carrots: "))
    num_holes = int(input("Enter the number of rabbit holes: "))

    game = RabbitGame(width, height, num_carrots, num_holes)
    game.generate_map()

    while not game.is_game_over():
        game.print_map()
        action = input("Enter your move (a/d/w/s/aw/as/dw/ds/p/j): ").lower()
        if action == 'p':
            game.pick_carrot()
        elif action == 'j':
            game.jump_rabbit()
        else:
            game.move_rabbit(action)
            game.deposit_carrot()

    print("Congratulations! Rabbit successfully deposited a carrot in a hole.")

if __name__ == "__main__":
    play_game()
