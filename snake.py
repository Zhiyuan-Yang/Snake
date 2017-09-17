#!/usr/bin/python
import curses
import thread
import threading
import time
import random


# TODO 
# press to speed up

snake_char = " "
snake_head_color = 1
fruit_char = " "
fruit_color = 2

def draw_snake(screen, nodes):
    for i in xrange(0, len(nodes)):
        attribute = (curses.color_pair(snake_head_color) | curses.A_REVERSE) if i == 0 else curses.A_REVERSE
        screen.addch(nodes[i][0], nodes[i][1]*2, snake_char, attribute)
        screen.addch(nodes[i][0], nodes[i][1]*2+1, snake_char, attribute)

def draw_fruit(screen, fruit):
    screen.addch(fruit[0], fruit[1]*2, fruit_char, curses.color_pair(fruit_color) | curses.A_REVERSE)
    screen.addch(fruit[0], fruit[1]*2+1, fruit_char, curses.color_pair(fruit_color) | curses.A_REVERSE)

class Snake:
    def __init__(self, max_width, max_height):
        self.nodes = [(0, 2), (0, 1), (0, 0)]
        self.direction = curses.KEY_RIGHT
        self.node_set = set()
        self.max_width = max_width
        self.max_height = max_height
        self.dead = False
        for node in self.nodes:
            self.node_set.add(node)

    def get_nodes(self):
        return self.nodes

    def is_dead(self):
        return self.dead

    def is_within_board(self, node):
        return 0 <= node[0] and node[0] < self.max_height and 0 <= node[1] and node[1]*2+1 < self.max_width

    def move(self):
        new_head = self.get_new_head(self.direction)
        if self.is_within_board(new_head) and not new_head in self.node_set:
            self.nodes.insert(0, new_head)
            self.node_set.remove(self.nodes.pop())
            self.node_set.add(new_head)
        else:
            self.dead = True

    def get_new_head(self, direction):
        (h, w) = self.nodes[0]
        if direction == curses.KEY_UP:
            return (h-1, w)
        elif direction == curses.KEY_DOWN:
            return (h+1, w)
        if direction == curses.KEY_LEFT:
            return (h, w-1)
        if direction == curses.KEY_RIGHT:
            return (h, w+1)

    def try_set_direction(self, direction):
        new_head = self.get_new_head(direction)
        if not new_head in self.node_set and self.is_within_board(new_head):
            self.direction = direction

    def try_eat_fruit(self, fruit):
        if self.get_new_head(self.direction) == fruit:
            self.nodes.insert(0, fruit)
            self.node_set.add(fruit)
            return True
        return False

    def get_node_set(self):
        return self.node_set

def choose_next_fruit(all_cell, snake):
    empty_cell = list(all_cell - snake.get_node_set())
    if len(empty_cell) == 0:
        return None
    return random.choice(empty_cell)
        
def main(screen):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(snake_head_color, curses.COLOR_RED, -1)
    curses.init_pair(fruit_color, curses.COLOR_GREEN, -1)

    (max_height, max_width) = screen.getmaxyx()
    snake = Snake(max_width, max_height)
    key = [None]
    all_cell = set()
    for i in xrange(0, max_height):
        for j in xrange(0, max_width/2):
            all_cell.add((i, j))
    fruit = choose_next_fruit(all_cell, snake)

    draw_snake(screen, snake.get_nodes())
    screen.getch()
    screen.nodelay(1)

    while True:
        new_direction = None
        key = screen.getch()
        if key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
            new_direction = key
        if new_direction != None:
            snake.try_set_direction(new_direction)
        if snake.try_eat_fruit(fruit):
            fruit = choose_next_fruit(all_cell, snake)
            if fruit == None:
                screen.addstr(max_height/2, max_width/2, "YOU WIN")
                break
        else:
            snake.move()

        screen.erase()
        draw_fruit(screen, fruit)
        draw_snake(screen, snake.get_nodes())
        screen.refresh()

        if snake.is_dead():
            screen.addstr(max_height/2, max_width/2, "GAME OVER")
            break
        time.sleep(0.1)

    screen.nodelay(0)
    screen.getch()

curses.wrapper(main)
