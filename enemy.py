import pygame
import random
from settings import *
from heapq import *


# vect = pygame.math.Vector2

class Cell:
    def __init__(self, x, y, g, h):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = self.app.cell_width // 2.4
        self.number = number
        self.color = self.set_color()
        self.direction = vect(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.shortest = []
        self.starting_pos = [pos.x, pos.y]
        self.speed = self.set_speed()
        self.image = self.load_img()

    def update(self):

        self.target = self.set_target()
        if self.target != self.grid_pos:
            if self.direction:
                self.pix_pos = self.pix_pos + self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_pos[0] = (self.pix_pos[0] - side +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - side +
                            self.app.cell_height // 2) // self.app.cell_height + 1

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos.x > cols // 2 and self.app.player.grid_pos.y > rows // 2:
                return vect(1, 1)
            if self.app.player.grid_pos.x > cols // 2 and self.app.player.grid_pos.y < rows // 2:
                return vect(1, rows - 3)
            if self.app.player.grid_pos.x < cols // 2 and self.app.player.grid_pos.y > rows // 2:
                return vect(cols - 3, 1)
            else:
                return vect(cols - 3, rows - 3)

    def draw(self):
        #pygame.draw.circle(self.app.screen, self.color, self.pix_pos, self.radius)
        self.app.screen.blit(self.image, (self.pix_pos.x - 12, self.pix_pos.y - 12))

        for cell in self.shortest:
            if cell != self.shortest[0] and cell != self.shortest[len(self.shortest) - 1]:
                pygame.draw.rect(self.app.screen, self.color,
                                 (self.get_pix_pos2(cell).x - self.app.cell_width // 2,
                                  self.get_pix_pos2(cell).y - self.app.cell_height // 2,
                                  self.app.cell_width, self.app.cell_height), 1)
        # if self.shortest:
        #    pygame.draw.rect(self.app.background, (177, 165, 84),
        #                     (self.shortest[0][0] * self.app.cell_width, self.shortest[0][1] * self.app.cell_height,
        #                     self.app.cell_width, self.app.cell_height), 1)

    def set_speed(self):
        if self.personality == 'speedy':
            speed = 2
        else:
            speed = 1
        return speed

    def time_to_move(self):
        if int(self.pix_pos.x + side // 2) % self.app.cell_width == 0:
            if self.direction == vect(1, 0) or self.direction == vect(-1, 0) or self.direction == vect(0, 0):
                return True
        if int(self.pix_pos.y + side // 2) % self.app.cell_height == 0:
            if self.direction == vect(0, 1) or self.direction == vect(0, -1) or self.direction == vect(0, 0):
                return True
        return False

    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_dir()
        elif self.personality == 'slow':
            #self.direction = self.get_path_dir(self.target)
            self.direction = self.get_random_dir()
        elif self.personality == 'speedy':
            self.direction = self.get_path_dir(self.target)
            #self.direction = self.get_random_dir()
        elif self.personality == 'scared':
            # self.direction = self.get_path_dir(self.target)
            self.direction = self.get_random_dir()

    def get_path_dir(self, target):
        next_cell = self.find_next_cell_in_path(target)
        if next_cell == self.grid_pos:
            return self.get_random_dir()
        x_dir = next_cell[0] - self.grid_pos[0]
        y_dir = next_cell[1] - self.grid_pos[1]
        return vect(x_dir, y_dir)

    def find_next_cell_in_path2(self, target):
        # path = self.BFS([self.grid_pos.x, self.grid_pos.y], [target.x, target.y])
        path = self.UCS([self.grid_pos.x, self.grid_pos.y], [target.x, target.y])
        next_cell = path[1]
        return next_cell

    def find_next_cell_in_path(self, target):
        path = []
        if self.app.algorithm_number % 3 == 0:

            path = self.BFS((self.grid_pos.x, self.grid_pos.y), [target.x, target.y])

        elif self.app.algorithm_number % 3 == 1:
            path = self.make_DFS([self.grid_pos.x, self.grid_pos.y], [target.x, target.y])

        elif self.app.algorithm_number % 3 == 2:
            path = self.BFS([self.grid_pos.x, self.grid_pos.y], [target.x, target.y])
        if len(path) <= 100:
            next_cell = [path[1][0], path[1][1]]
        else:
            next_cell = [self.grid_pos[0], self.grid_pos[1]]
        return next_cell

    def BFS(self, start, target):
        grid = self.make_grid()
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + current[0] < len(grid[0]):
                        if 0 <= neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[int(next_cell[1])][int(next_cell[0])] != 1:
                                    if next_cell not in queue:
                                        queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        return self.shortest_path(start, target, path)

    def make_grid(self):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        return grid

    def shortest_path(self, start, target, path):
        self.shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    self.shortest.insert(0, step["Current"])
                    #print(self.shortest)
            # self.draw_short_path(sefshortest)
            #a = 1
            #print(a)
        return self.shortest

    def UCS(self, start, target):
        grid = self.make_grid()
        queue = [[0, start]]
        path = []
        visited = []
        key = 0
        while queue:
            key += 1
            queue = sorted(queue)
            current = queue[-1]
            del queue[-1]
            visited.append(current[1])
            current[0] *= -1
            if current[1] == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + current[1][0] < len(grid[0]):
                        if 0 <= neighbour[1] + current[1][1] < len(grid):
                            next_cell = [neighbour[0] + current[1][0], neighbour[1] + current[1][1]]
                            if next_cell not in visited:
                                if grid[int(next_cell[1])][int(next_cell[0])] != 1:
                                    if [(current[0] + 1) * -1, next_cell] not in queue:
                                        queue.append([(current[0] + 1) * -1, next_cell])
                                    path.append({"Current": current[1], "Next": next_cell})
        return self.shortest_path(start, target, path)

    def calc_h(self, cur, target):
        return abs(cur[0] - target[0]) + abs(cur[1] - target[1])

    def AStar(self, start, target):
        grid = self.make_grid()
        start_cell = Cell(start[0], start[1], 0, self.calc_h(start, target))
        queue = [[0, start_cell]]
        cost_visited = {start_cell: 0}
        path = []
        visited = []

        while queue:
            queue = sorted(queue, key=lambda cell: cell.f)
            cur_prior, cur_cell = queue[-1]
            del queue[-1]
            visited.append(cur_cell)
            cur_prior *= -1
            if cur_cell.x == target[0] and cur_cell.y == target[1]:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + cur_cell.x < len(grid[0]):
                        if 0 <= neighbour[1] + cur_cell.y < len(grid):
                            next_cell = Cell(neighbour[0] + cur_cell.x, neighbour[1] + cur_cell.y,
                                             cur_cell.g + 1, self.calc_h([neighbour[0] + cur_cell.x,
                                                                          neighbour[1] + cur_cell.y], target))
                            if next_cell not in visited:
                                if grid[int(next_cell.y)][int(next_cell.x)] != 1:
                                    if next_cell not in cost_visited \
                                            or cost_visited[next_cell] > next_cell.g:
                                        queue.append([(next_cell.g + next_cell.h) * -1, next_cell])
                                        cost_visited[next_cell] = next_cell.g
                                        path.append({"Current": cur_cell, "Next": next_cell})
        return self.shortest_path(start, target, path)

    def AStar2(self, start, target):
        grid = self.make_grid()
        start_cell = Cell(start[0], start[1], 0, self.calc_h(start, target))
        queue = []
        heappush(queue, (0, start_cell))
        heappush(queue, (0, start_cell))
        cost_visited = {start_cell: 0}
        path = []
        visited = []

        while queue:
            cur_prior, cur_cell = heappop(queue)
            visited.append(cur_cell)

            if cur_cell.x == target[0] and cur_cell.y == target[1]:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + cur_cell.x < len(grid[0]):
                        if 0 <= neighbour[1] + cur_cell.y < len(grid):
                            next_cell = Cell(neighbour[0] + cur_cell.x, neighbour[1] + cur_cell.y,
                                             cur_cell.g + 1, self.calc_h([neighbour[0] + cur_cell.x,
                                                                          neighbour[1] + cur_cell.y], target))
                            if next_cell not in visited:
                                if grid[int(next_cell.y)][int(next_cell.x)] != 1:
                                    if next_cell not in cost_visited or cost_visited[next_cell] > next_cell.g:
                                        w1 = int(next_cell.g + next_cell.h)
                                        heappush(queue, (w1, next_cell))
                                        cost_visited[next_cell] = next_cell.g
                                        path.append({"Current": cur_cell, "Next": next_cell})
        return self.shortest_path(start, target, path)

    def AStar3(self, start, target):
        grid = self.make_grid()
        start_cell = (start[0], start[1])
        target_cell = (target[0], target[1])
        queue = []
        heappush(queue, (0, start_cell))
        cost_visited = {start_cell: 0}
        path = []
        visited = []

        while queue:
            cur_prior, cur_cell = heappop(queue)
            visited.append(cur_cell)

            if cur_cell[0] == target[0] and cur_cell[1] == target[1]:
                queue = []
                continue
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if 0 <= neighbour[0] + cur_cell[0] < len(grid[0]):
                        if 0 <= neighbour[1] + cur_cell[1] < len(grid):
                            # next_cell = Cell(neighbour[0] + cur_cell.x, neighbour[1] + cur_cell.y,
                            #                 cur_cell.g + 1, self.calc_h([neighbour[0] + cur_cell.x,
                            #                                              neighbour[1] + cur_cell.y], target))
                            next_cell = (neighbour[0] + cur_cell[0], neighbour[1] + cur_cell[1])
                            new_cost = cost_visited[cur_cell] + 1
                            if next_cell not in visited:
                                if grid[int(next_cell[1])][int(next_cell[0])] != 1:
                                    if next_cell not in cost_visited or cost_visited[next_cell] > new_cost:
                                        priority = new_cost + self.calc_h(next_cell, target_cell)
                                        # w1 = int(next_cell.g + next_cell.h)
                                        heappush(queue, (int(priority), next_cell))
                                        cost_visited[next_cell] = new_cost
                                        path.append({"Current": cur_cell, "Next": next_cell})
        sh_path = self.shortest_path(start, target, path)
        return sh_path

    def astar(self, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""
        maze = self.make_grid()

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    print(path)
                    current = current.parent
                return path[::-1]  # Return reversed path
            else:
                print('AAaaaaaaaaa')

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

                # Get node position
                node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[int(node_position[1])][int(node_position[0])] == 1:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g < open_node.g:
                        open_node.g = child.g
                        open_node.parent = child.parent


                # Add the child to the open list
                open_list.append(child)

        # def AStar2(self, start, target):

    #    start = (0, 7)
    #    goal = (22, 7)
    #    queue = []
    #    heappush(queue, (0, start))
    #    cost_visited = {start: 0}
    #    visited = {start: None}
    #
    #    if queue:
    #        cur_cost, cur_node = heappop(queue)
    #        if cur_node == goal:
    #            queue = []
    #            continue
    #
    #        next_nodes = graph[cur_node]
    #        for next_node in next_nodes:
    #            neigh_cost, neigh_node = next_node
    #            new_cost = cost_visited[cur_node] + neigh_cost
    #
    #            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
    #                priority = new_cost + heuristic(neigh_node, goal)
    #                heappush(queue, (priority, neigh_node))
    #                cost_visited[neigh_node] = new_cost
    #                visited[neigh_node] = cur_node
    #

    def make_DFS(self, start, target):
        grid = self.make_grid()
        visited = []
        path = []
        self.DFS(start, target, visited, path, grid)
        return self.shortest_path(start, target, path)

    def DFS(self, current, target, visited, path, grid):
        visited.append(current)
        if current == target:
            return
        neighbours = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        for neighbour in neighbours:
            if 0 <= neighbour[0] + current[0] < len(grid[0]):
                if 0 <= neighbour[1] + current[1] < len(grid):
                    next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                    if grid[int(next_cell[1])][int(next_cell[0])] != 1:
                        if next_cell not in visited:
                            path.append({"Current": current, "Next": next_cell})
                            self.DFS(next_cell, target, visited, path, grid)

    def get_random_dir(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_pos = vect(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vect(x_dir, y_dir)

    def get_pix_pos(self):
        return vect((self.grid_pos.x * self.app.cell_width) + side // 2 + self.app.cell_width // 2,
                    (self.grid_pos.y * self.app.cell_height) + side // 2 +
                    self.app.cell_height // 2)

    def get_pix_pos2(self, grid_pos):
        return vect((grid_pos[0] * self.app.cell_width) + side // 2 + self.app.cell_width // 2,
                    (grid_pos[1] * self.app.cell_height) + side // 2 +
                    self.app.cell_height // 2)

    def set_color(self):
        if self.number == 0:
            return 255, 51, 255
        elif self.number == 1:
            return 0, 255, 0
        elif self.number == 2:
            return 0, 204, 204
        elif self.number == 3:
            return 102, 0, 204

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "slow"
        elif self.number == 3:
            return "slow"
        # elif self.number == 2:
        #    return "random"
        # elif self.number == 3:
        #    return "scared"

    def load_img(self):
        if self.number == 0:
            return pygame.transform.scale(pygame.image.load('img/Blinky.png'), (24, 24))
        elif self.number == 1:
            return pygame.transform.scale(pygame.image.load('img/Inky.png'), (24, 24))
        elif self.number == 2:
            return pygame.transform.scale(pygame.image.load('img/Pinky.png'), (24, 24))
        elif self.number == 3:
            return pygame.transform.scale(pygame.image.load('img/Clyde.png'), (24, 24))
