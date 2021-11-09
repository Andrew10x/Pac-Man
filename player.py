from heapq import *
from random import randint
from minimax import *

import pygame
from settings import *


# vect = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.target = self.app.fruit
        self.grid = self.make_grid()
        self.starting_pos = [pos[0], pos[1]]
        self.grid_pos = vect(pos[0], pos[1])
        self.pix_pos = self.get_pix_pos()
        self.root_node = None
        self.direction = vect(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.walk_right = None
        self.walk_left = None
        self.walk_up = None
        # self.fruit = vect(1, 23)
        self.walk_down = None
        self.anim_count = 0
        self.shortest = []

        self.load()
        self.speed = 2
        self.lives = 3

    def load(self):
        size = self.app.cell_width - 2
        self.walk_right = [pygame.transform.scale(pygame.image.load('img/r1.png'), (size, size)),
                           pygame.transform.scale(pygame.image.load('img/r2.png'), (size, size)),
                           pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]
        self.walk_left = [pygame.transform.scale(pygame.image.load('img/r11.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r21.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]
        self.walk_up = [pygame.transform.scale(pygame.image.load('img/r12.png'), (size, size)),
                        pygame.transform.scale(pygame.image.load('img/r22.png'), (size, size)),
                        pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]
        self.walk_down = [pygame.transform.scale(pygame.image.load('img/r14.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r24.png'), (size, size)),
                          pygame.transform.scale(pygame.image.load('img/r3.png'), (size, size))]

    def update(self):
        if self.anim_count >= 36:
            self.anim_count = 0
        else:
            self.anim_count += 6
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            self.move()
            if self.stored_direction is not None:
                self.direction = self.stored_direction

            self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - side +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - side +
                            self.app.cell_height // 2) // self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()

        if self.on_friut():
            self.eat_fruit()

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
        return self.shortest

    def find_next_cell_in_path(self, target):
        path = []

        path = self.AStar3((self.grid_pos.x, self.grid_pos.y), (target.x, target.y))
        # path = self.BFS((self.grid_pos.x, self.grid_pos.y), [target.x, target.y])
        if len(path) >= 2:
            next_cell = [path[1][0], path[1][1]]
        else:
            next_cell = [self.grid_pos[0], self.grid_pos[1]]
        return next_cell

    def move1(self):
        self.direction = self.get_path_dir(self.app.fruit)

    def minimax_move(self, matrix):
        # current_coord = self.get_matrix_coordinates()
        # if current_coord == self.target:
        #     self.target = None
        # if self.target is None:  # and self.time_counter % 50 == 0:
        #self.set_new_target()
        self.target = self.app.fruit
        if self.target is not None:
            state = GameState(matrix)
            enemies_coords = state.get_enemies_positions()
            if self.root_node is not None:
                nodes = [item for sublist in
                         list(map(lambda child: child.children, self.root_node.children))
                         for item in sublist]
                big_flag = False
                for last_node in nodes:
                    last_enemies_coords = last_node.state.get_enemies_positions()
                    flag = True
                    for enemies_coord in enemies_coords:
                        if enemies_coord not in last_enemies_coords:
                            flag = False
                            break

                    if flag:
                        self.root_node = last_node
                        new_grid = self.make_grid()
                        new_grid[int(self.grid_pos[1])][int(self.grid_pos[0])] = 5
                        for e_p in self.app.e_pos:
                            self.grid[int(e_p[0])][int(e_p[1])] = 6

                        generate_tree_recurs(last_node, 1, new_grid, self.target)
                        print('FOUND')
                        big_flag = True
                        break
                # if not big_flag:
                self.root_node = generate_tree(state, self.target)
            else:
                self.root_node = generate_tree(state, self.target)
            best_value = minimax(self.root_node, -math.inf, math.inf, 0)
            #best_value = expectimax(self.root_node, 0)

            pacman_position = self.grid_pos
            for child in self.root_node.children:
                if child.value == best_value:
                    new_position = child.state.get_pacman_position()
                    delta = (-pacman_position[0] + new_position[0],
                             -pacman_position[1] + new_position[1])
                    return delta
                    #new_direction = self.vector_dict.get(delta)
                    #if new_direction is not None:
                    #    self.direction = new_direction
                    #else:
                    #    self.set_new_target()
                    #break
        self.move()

    def minimax_move2(self, matrix):
        self.target = self.app.fruit
        if self.target is not None:
            state = GameState(matrix)
            enemies_coords = state.get_enemies_positions()
            if self.root_node is not None:
                nodes = [item for sublist in
                         list(map(lambda child: child.children, self.root_node.children))
                         for item in sublist]
                big_flag = False
                for last_node in nodes:
                    last_enemies_coords = last_node.state.get_enemies_positions()
                    flag = True
                    for enemies_coord in enemies_coords:
                        if enemies_coord not in last_enemies_coords:
                            flag = False
                            break

                    if flag:
                        self.root_node = last_node
                        self.grid[int(self.grid_pos[0])][int(self.grid_pos[1])] = 2
                        for e_p in self.app.e_pos:
                            self.grid[int(e_p[0])][int(e_p[1])] = 3
                        generate_tree_recurs(last_node, 1, self.grid, self.target)
                        print('FOUND')
                        big_flag = True
                        break
                # if not big_flag:
                self.root_node = generate_tree(state, self.target)
            else:
                self.root_node = generate_tree(state, self.target)
            best_value = minimax(self.root_node, -math.inf, math.inf, 0)
            # best_value = expectimax(self.root_node, 0)

            pacman_position = self.grid_pos
            for child in self.root_node.children:
                if child.value == best_value:
                    new_position = child.state.get_pacman_position()
                    delta = [-pacman_position[0] + new_position[0],
                             -pacman_position[1] + new_position[1]]
                    print(delta)
                    return delta
                    # new_direction = self.vector_dict.get(delta)
                    # if new_direction is not None:
                    #    self.direction = new_direction
                    # else:
                    #    self.set_new_target()
                    # break
        # self.move()

    def get_path_dir(self, target):
        # next_cell = self.find_next_cell_in_path(target)
        # x_dir = next_cell[0] - self.grid_pos[0]
        # y_dir = next_cell[1] - self.grid_pos[1]
        # return vect(x_dir, y_dir)
        #self.grid[int(self.grid_pos[0])][int(self.grid_pos[1])] = 5
        #self.grid[int(self.app.e_pos[0][0])][int(self.app.e_pos[0][1])] = 6
        # for e_p in self.app.e_pos:
        #    self.grid[int(e_p[0])][int(e_p[1])] = 6
        #self.grid[int(self.app.e_pos[0][0])][int(self.app.e_pos[0][1])] = 6
        new_grid = self.make_grid()
        new_grid[int(self.grid_pos[1])][int(self.grid_pos[0])] = 5
        new_grid[int(self.app.e_pos[0][1])][int(self.app.e_pos[0][0])] = 6
        #for e_p in self.app.e_pos:
        #  new_grid[int(e_p[0])][int(e_p[1])] = 6
        #new_grid[int(self.app.e_pos[0][1])][int(self.app.e_pos[0][0])] = 6
        dir = self.minimax_move(new_grid)
        print(dir)
        return vect(dir[0], dir[1])

    def calc_h(self, cur, target):
        return abs(cur[0] - target[0]) + abs(cur[1] - target[1])

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

        return self.shortest_path(start, target, path)

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

    def draw(self):
        pac_x = int(self.pix_pos.x - self.app.cell_width // 2)
        pac_y = int(self.pix_pos.y - self.app.cell_height // 2)
        pac_pos = vect(pac_x, pac_y)
        if self.direction == (0, -1):
            self.app.screen.blit(self.walk_up[self.anim_count // 14], pac_pos)
        elif self.direction == (-1, 0):
            self.app.screen.blit(self.walk_left[self.anim_count // 14], pac_pos)
        elif self.direction == (0, 1):
            self.app.screen.blit(self.walk_down[self.anim_count // 14], pac_pos)
        else:
            self.app.screen.blit(self.walk_right[self.anim_count // 14], pac_pos)
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, (230, 250, 70), (30 + x * 17, height - 15), 7)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if self.time_to_move():
                return True
        else:
            return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def on_friut(self):
        if self.grid_pos == self.app.fruit:
            if self.time_to_move():
                return True
        else:
            return False

    def eat_fruit(self):
        pos = randint(0, len(self.app.cells) - 1)
        self.app.fruit = self.app.cells[pos]
        self.current_score += 10

    def move(self, dir=0):
        if dir == 0:
            self.stored_direction = self.get_path_dir(self.app.fruit)
        else:
            self.stored_direction = dir

    # def move(self, dir):
    #    self.stored_direction = dir

    def get_pix_pos(self):
        return vect((self.grid_pos[0] * self.app.cell_width) + side // 2 + self.app.cell_width // 2,
                    (self.grid_pos[1] * self.app.cell_height) +
                    side // 2 + self.app.cell_height // 2)

    def time_to_move(self):
        if int(self.pix_pos.x + side // 2) % self.app.cell_width == 0:
            if self.direction == vect(1, 0) or self.direction == vect(-1, 0) or self.direction == vect(0, 0):
                return True
        if int(self.pix_pos.y + side // 2) % self.app.cell_height == 0:
            if self.direction == vect(0, 1) or self.direction == vect(0, -1) or self.direction == vect(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vect(self.grid_pos + self.direction) == wall:
                return False
        return True
