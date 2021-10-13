# maze module

import numpy as np
import matplotlib.pyplot as plt
import maze_utils as util


class maze:
    def __init__(self, x_size=14, y_size=14):
        self.y_size = y_size
        self.x_size = x_size
        self.maze_array = np.full((self.y_size, self.x_size), -100)
        self.cmap = 'gray'
        self.q_values = np.zeros((self.y_size, self.x_size, 4))
        self.destination = [1, 0]
        self.is_shift_held = False

        for x in range(1, self.x_size - 1):
            for y in range(1, self.y_size - 1):
                util.remove_wall(x, y, self)

        self.current_x, self.current_y = util.get_starting_location(self)
        self.set_destination(self.destination[0], self.destination[1])

    def edit(self):
        # GUI Maze editor
        fig = plt.figure(figsize=(7, round(7 * self.x_size / self.y_size)))
        plt.imshow(self.maze_array, cmap=self.cmap)
        plt.rcParams['backend'] = 'TkAgg'

        def on_MB_press(event):
            if self.is_shift_held:
                self.set_destination(
                    int(round(event.xdata)), int(round(event.ydata)))
            else:
                if util.is_wall(int(round(event.xdata)),
                                int(round(event.ydata)), self):
                    util.remove_wall(int(round(event.xdata)),
                                     int(round(event.ydata)), self)
                elif not util.is_wall(int(round(event.xdata)),
                                      int(round(event.ydata)), self):
                    util.add_wall(int(round(event.xdata)),
                                  int(round(event.ydata)), self)

            self.current_x, self.current_y = int(round(event.xdata)), int(round(event.ydata))

            plt.clf()
            plt.imshow(self.maze_array, cmap=self.cmap)
            plt.title('maze editor')
            plt.draw()
        fig.canvas.mpl_connect('button_press_event', on_MB_press)

        def on_key_press(event):

            if event.key == 'shift':
                self.is_shift_held = True

            if event.key == 'i':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 0, self)
            elif event.key == 'l':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 1, self)
            elif event.key == 'k':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 2, self)
            elif event.key == 'j':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 3, self)

            if event.key == 'i' or event.key == 'l' or event.key == 'k' or event.key == 'j':
                if util.is_wall(self.current_x, self.current_y, self):
                    util.remove_wall(self.current_x, self.current_y, self)
                elif not util.is_wall(self.current_x, self.current_y, self):
                    util.add_wall(self.current_x, self.current_y, self)

            plt.clf()
            plt.imshow(self.maze_array, cmap=self.cmap)
            plt.title('maze editor')
            plt.draw()
        fig.canvas.mpl_connect('key_press_event', on_key_press)

        def on_key_release(event):
            if event.key == 'shift':
                self.is_shift_held = False
        fig.canvas.mpl_connect('key_release_event', on_key_release)

        plt.title("maze editor (use movement keys 'I', 'J', 'K' 'L' for faster editing),\n use shift+click to move destination")
        plt.show()


    def set_destination(self, x, y):
        util.add_wall(self.destination[0], self.destination[1], self)
        self.maze_array[int(round(y)), int(round(x))] = 100
        self.destination = [x, y]


    def solve(self):
        fig = plt.figure(figsize=(7, round(7 * self.x_size / self.y_size)))
        plt.imshow(self.maze_array, cmap=self.cmap)
        plt.rcParams['backend'] = 'TkAgg'

        def on_MB_press(event):
            x, y = int(round(event.xdata)), int(round(event.ydata))
            final_path = util.get_shortest_path(x, y, self)
            maze = self.maze_array.copy()
            for step in final_path:
                maze[step[1], step[0]] = 50
            plt.clf()
            plt.imshow(maze, cmap=self.cmap)
            plt.title('Path from ({}, {}) to ({}, {})'.format(
                x, y, self.destination[0], self.destination[1]))
            plt.draw()

        fig.canvas.mpl_connect('button_press_event', on_MB_press)
        plt.title('click to set source')
        plt.show()


    def reward(self, x, y):
        return (self.maze_array[y, x])


    def play(self):
        fig = plt.figure(figsize=(7, round(7 * self.x_size / self.y_size)))
        plt.imshow(self.maze_array, cmap=self.cmap)
        plt.rcParams['backend'] = 'TkAgg'

        def on_MB_press(event):
            self.current_x, self.current_y = int(round(event.xdata)), int(round(event.ydata))
            maze = self.maze_array.copy()

            if util.is_terminal_state(self.current_x, self.current_y, self):
                self.current_x, self.current_y = util.get_starting_location(self)

            maze[self.current_y, self.current_x] = 50
            plt.clf()
            plt.imshow(maze, cmap=self.cmap)
            plt.title('play')
            plt.draw()
        fig.canvas.mpl_connect('button_press_event', on_MB_press)

        def on_key_press(event):

            maze = self.maze_array.copy()

            if event.key == 'i':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 0, self)
            elif event.key == 'l':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 1, self)
            elif event.key == 'k':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 2, self)
            elif event.key == 'j':
                self.current_x, self.current_y = util.get_next_location(
                    self.current_x, self.current_y, 3, self)

            if util.is_terminal_state(self.current_x, self.current_y, self):
                self.current_x, self.current_y = util.get_starting_location(self)

            maze[self.current_y, self.current_x] = 50
            plt.clf()
            plt.imshow(maze, cmap=self.cmap)
            plt.title('play')
            plt.draw()

        fig.canvas.mpl_connect('key_press_event', on_key_press)
        plt.title("'I', 'J', 'K', 'L' are movement keys")
        plt.show()
