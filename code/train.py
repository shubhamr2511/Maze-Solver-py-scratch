# train module

import numpy as np
import maze_utils as util

class train:
    def __init__(
            self,
            maze,
            epsilon=0.9,
            discount_factor=0.9,
            learing_rate=0.9,
            iterations=1000):

        for episode in range(iterations):

            current_x, current_y = util.get_starting_location(maze)

            while not util.is_terminal_state(current_x, current_y, maze):
                action = util.get_next_action(
                    current_x, current_y, epsilon, maze.q_values)

                previous_x, previous_y = current_x, current_y
                
                current_x, current_y = util.get_next_location(
                    current_x, current_y, action, maze)

                reward = maze.reward(current_x, current_y)
                previous_q_value = maze.q_values[previous_y,
                                                 previous_x, action]

                temporal_difference = reward + \
                    (discount_factor * np.max(maze.q_values[current_y, current_x])) - previous_q_value

                new_q_value = previous_q_value + learing_rate * temporal_difference
                maze.q_values[previous_y, previous_x, action] = new_q_value

        print('Training Complete!')

    # More functions to be added
