import pygame
from copy import deepcopy
import numpy as np
import random
import time

class Tetrominos(object):
    def __init__(self, column, row, shape, shapes, shape_colors):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


class Tetris:
    def __init__(self):
        ## SHAPE FORMATS
        self.S = [['.....',
              '......',
              '..00..',
              '.00...',
              '.....'],
             ['.....',
              '..0..',
              '..00.',
              '...0.',
              '.....']]

        self.Z = [['.....',
              '.....',
              '.00..',
              '..00.',
              '.....'],
             ['.....',
              '..0..',
              '.00..',
              '.0...',
              '.....']]

        self.I = [['..0..',
              '..0..',
              '..0..',
              '..0..',
              '.....'],
             ['.....',
              '0000.',
              '.....',
              '.....',
              '.....']]

        self.O = [['.....',
              '.....',
              '.00..',
              '.00..',
              '.....']]

        self.J = [['.....',
              '.0...',
              '.000.',
              '.....',
              '.....'],
             ['.....',
              '..00.',
              '..0..',
              '..0..',
              '.....'],
             ['.....',
              '.....',
              '.000.',
              '...0.',
              '.....'],
             ['.....',
              '..0..',
              '..0..',
              '.00..',
              '.....']]

        self.L = [['.....',
              '...0.',
              '.000.',
              '.....',
              '.....'],
             ['.....',
              '..0..',
              '..0..',
              '..00.',
              '.....'],
             ['.....',
              '.....',
              '.000.',
              '.0...',
              '.....'],
             ['.....',
              '.00..',
              '..0..',
              '..0..',
              '.....']]

        self.T = [['.....',
              '..0..',
              '.000.',
              '.....',
              '.....'],
             ['.....',
              '..0..',
              '..00.',
              '..0..',
              '.....'],
             ['.....',
              '.....',
              '.000.',
              '..0..',
              '.....'],
             ['.....',
              '..0..',
              '.00..',
              '..0..',
              '.....']]

        self.shapes = [self.S, self.Z, self.I, self.O, self.J, self.L, self.T]
        self.shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 120, 0), (0, 0, 255), (180, 0, 180)]

        pygame.init()
        self.screenHeight = 700
        self.screenWidth = 700
        self.playWidth = 300
        self.playHeight = 600
        self.cols = 10
        self.rows = 20
        self.block_size = 30

        self.top_left_x = 100
        self.top_left_y = (self.screenHeight - self.playHeight)

        ## GAME VARS
        self.locked_pos = {}
        self.grid = self.create_grid(self.locked_pos)  ## play area
        self.change_piece = False
        self.game_over = False
        self.curr_tetromino = self.get_shape()
        self.next_tetromino = self.get_shape()
        self.score = 0


    def reset(self):
        grid = [[(20, 20, 20) for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False
        self.locked_pos = {}
        self.grid = self.create_grid(self.locked_pos)  ## play area
        self.change_piece = False
        self.game_over = False
        self.curr_tetromino = self.get_shape()
        self.next_tetromino = self.get_shape()
        self.score = 0
        return self.grid

## =============================== RENDERING GUI ===============================
    def create_grid(self, locked_pos = {}):
        grid = [[(20, 20, 20) for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c
        return grid


    def draw_grid(self, surface):
        sx = self.top_left_x
        sy = self.top_left_y

        for j in range(self.rows):
            pygame.draw.line(surface, (160, 160, 160), (sx, sy + j*self.block_size), (sx + self.playWidth, sy + j*self.block_size))
        for j in range(self.cols):
            pygame.draw.line(surface, (160, 160, 160), (sx + j*self.block_size, sy), (sx + j*self.block_size, sy + self.playHeight))


    def draw_window(self, surface, grid):
        surface.fill((20, 20, 20))

        pygame.font.init()
        font = pygame.font.SysFont("comicsans", 60)
        label = font.render("TETRIS", 1, (255, 255, 255))

        surface.blit(label, (self.top_left_x + self.playWidth//2 - (label.get_width()//2), 30))

        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(surface, grid[i][j], (self.top_left_x + j*self.block_size, self.top_left_y + i*self.block_size, self.block_size, self.block_size), 0)

        pygame.draw.rect(surface, (240, 160, 0), (self.top_left_x, self.top_left_y, self.playWidth, self.playHeight), 5)
        pygame.draw.line(surface, (255, 255, 255), (500, 0), (500, self.screenHeight), 3)
        self.draw_grid(surface)


    def draw_next_tetromino(self, surface, tetromino, score=0):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", 24)
        label = font.render("Next Shape:", 1, (255, 255, 255))

        label_score = font.render("SCORE: " + str(score), 1, (255, 255, 255))

        format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, tetromino.color, (520 + j*self.block_size, 300 + i*self.block_size, self.block_size, self.block_size))
        surface.blit(label, (520, 270))
        surface.blit(label_score, (520, 100))


    def render(self):
        win = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.draw_window(win, self.grid)
        self.draw_next_tetromino(win, self.next_tetromino, self.score)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()


## ======================== GAME LOGIC =========================================
    def get_shape(self):
        return Tetrominos(5, 0, random.choice(self.shapes), self.shapes, self.shape_colors)


    def render_tetrominos(self, tetromino):
        positions = []
        format = tetromino.shape[tetromino.rotation % len(tetromino.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((tetromino.x + j, tetromino.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        return positions


    def collison_check(self, tetromino, grid):
        accepted_pos = [[(j, i) for j in range(self.cols) if grid[i][j] == (20, 20, 20)] for i in range(self.rows)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        positions = self.render_tetrominos(tetromino)
        for pos in positions:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True


    def is_valid_position(self, positions, grid):
        accepted_pos = [[(j, i) for j in range(self.cols) if grid[i][j] == (20, 20, 20)] for i in range(self.rows)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        for pos in positions:
            if pos not in accepted_pos:
                return False
        return True


    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False


    def clear_rows(self, grid, locked_pos):
        inc = 0
        for i in range(len(grid)-1, -1, -1):
            row = grid[i]
            if (20, 20, 20) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked_pos[(j, i)]
                    except:
                        continue

        if inc > 0:
            for key in sorted(list(locked_pos), key = lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked_pos[newKey] = locked_pos.pop(key)
        return inc


    def drop(self, loc, rotation):
        self.curr_tetromino.x = loc
        self.curr_tetromino.rotation = rotation

        while True:
            self.curr_tetromino.y += 1
            if not self.collison_check(self.curr_tetromino, self.grid) and self.curr_tetromino.y > 0:
                self.curr_tetromino.y -= 1
                self.change_piece = True
                break

        tetromino_pos = self.render_tetrominos(self.curr_tetromino)
        # print(tetromino_pos)                                                  #####

        for i in range(len(tetromino_pos)):
            x, y = tetromino_pos[i]
            if y > -1:
                self.grid[y][x] = self.curr_tetromino.color

        if self.change_piece:
            for pos in tetromino_pos:
                # p = (pos[0], pos[1])
                self.locked_pos[pos] = self.curr_tetromino.color

            self.curr_tetromino = self.next_tetromino
            self.next_tetromino = self.get_shape()
            self.change_piece = False
            self.score += self.clear_rows(self.grid, self.locked_pos)
            self.grid = self.create_grid(self.locked_pos)

        self.render()

        if self.check_lost(self.locked_pos):
            self.game_over = True


######################################### AI LOGIC #################################
    def print_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print(self.grid[i][j], end=" | ")
            print()


    def number_of_holes(self, grid):
        holes = 0

        for i in range(self.cols):
            col = self.rows * [0]
            block_in_col = False

            for j in range(self.rows - 1, -1, -1):
                if grid[j][i] == (20, 20, 20):
                    col[j] = 0
                else:
                    col[j] = 1

            for k in range(len(col)):
                if col[k] == 1:
                    block_in_col = True
                elif block_in_col and col[k] == 0:
                    holes += 1
            # print(holes, col)
        return holes


    def get_height(self, grid):
        heights = []

        for i in range(self.cols):
            height = 0
            for j in range(self.rows - 1, -1, -1):
                if grid[j][i] != (20, 20, 20):
                    height = 20 - j
            heights.append(height)
        # print(heights)
        return heights


    def bumpiness(self, heights):
        total_bumpiness = 0
        max_bumpiness = 0
        for i in range(len(heights)-1):
            total_bumpiness += abs(heights[i+1] - heights[i])
            if max_bumpiness > abs(heights[i+1] - heights[i]):
                max_bumpiness = abs(heights[i+1] - heights[i])

        return total_bumpiness, max_bumpiness


    def get_grid_props(self, grid, locked_pos):
        lines = self.clear_rows(grid, locked_pos)
        heights = self.get_height(grid)
        total_bumpiness, max_bumpiness = self.bumpiness(heights)
        holes = self.number_of_holes(grid)
        if sum(heights) != 0:
            avg_height = sum(heights) / len([x for x in heights if x != 0])
        else:
            avg_height = 0
        # print(lines, heights, avg_height, total_bumpiness, holes, sep='  ||  ')  #####
        return [lines, avg_height, total_bumpiness, holes]


    def get_next_states(self):
        next_states = {}

        for rot in range(len(self.curr_tetromino.shape)):
            # print(self.curr_tetromino.shape[self.curr_tetromino.rotation])    #####
            for x in range(self.cols):
                self.curr_tetromino.x = x
                self.curr_tetromino.y = 0
                next_grid = deepcopy(self.grid)
                next_locked_pos = deepcopy(self.locked_pos)

                while True:
                    self.curr_tetromino.y += 1
                    if not self.collison_check(self.curr_tetromino, self.grid) and self.curr_tetromino.y > 0:
                        self.curr_tetromino.y -= 1
                        break

                tetromino_pos = self.render_tetrominos(self.curr_tetromino)
                if self.is_valid_position(tetromino_pos, self.grid):
                    for i in range(len(tetromino_pos)):
                        p, q = tetromino_pos[i]
                        next_grid[q][p] = self.curr_tetromino.color
                    # print(tetromino_pos, self.curr_tetromino.x)               #####
                    next_states[(x, rot)] = self.get_grid_props(next_grid, next_locked_pos)

            self.curr_tetromino.rotation += 1

        return next_states


    def reward(self, state):
        # r_wts = np.array([10, -5, -2, -3.5])
        r_wts = np.array([0.76, -0.51, -0.18, -0.36])
        state = np.array(state)

        reward = state @ r_wts.T

        return reward


########################################### LSPI #########################################################

def main():
    env = Tetris()

    GAMMA = 1
    ALPHA = 1
    EPISLON = 1
    EPSILON_TAPER = 0.01
    EPISODES = 1000

    # for i in range(EPISODES):
    s = env.reset()

    # next_states = env.get_next_states()
    # for k in next_states.keys():
    #         print(k, " --> ", next_states[k], ' ==>> ', env.reward(next_states[k]) )

    while not env.game_over:
    # for steps in range(7):
        next_states = env.get_next_states()
        r = np.ones((10, 4)) * float('-inf')
        for k in next_states.keys():
            # print(k, " --> ", next_states[k], ' ==>> ', env.reward(next_states[k]) )
            i, j = k
            r[i][j] = env.reward(next_states[k])

        best_loc, best_rot = np.unravel_index(r.argmax(), r.shape)
        # print(f"[{best_loc} || {best_rot}]")

        print(next_states[(best_loc, best_rot)])
        env.drop(best_loc, best_rot)
        # for k in env.locked_pos.keys():
        #     print(k, " --> ", env.locked_pos[k])
        # env.clear_rows(env.grid, env.locked_pos)
        # env.render()
        time.sleep(0.3)


if __name__ == '__main__':
    main()
