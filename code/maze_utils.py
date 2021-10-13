# Utility module : contains helper functions

import numpy as np

actions = ['up', 'right', 'down', 'left']  # actions with their indices.


def add_wall(x, y, maze):
    # add new wall at (x, y).
    maze.maze_array[int(y), int(x)] = -100


def remove_wall(x, y, maze):
    # removes wall at (x,y).
    if 0 < x < maze.x_size - 1 and 0 < y < maze.y_size - 1:
        maze.maze_array[int(y), int(x)] = -1
        

def is_wall(x, y, maze):
    # Return True if there is a wall at (x, y).
    if maze.maze_array[int(y), int(x)] == -100:

        return True
    else:

        return False


def is_terminal_state(x, y, maze):
    # Returns True if Agent hits wall or destination.
    if maze.maze_array[y, x] == -1:

        return False
    else:

        return True


def get_next_action(x, y, epsilon, q_values):
    # return best action for current position using Q values.
    if np.random.random() < epsilon:

        return np.argmax(q_values[y, x])
    else:

        return np.random.randint(4)


def get_next_location(current_x, current_y, action, maze):
    # returns new location based on action and current location.
    new_x, new_y = current_x, current_y

    if actions[action] == 'up' and current_y > 0:
        new_y -= 1
    elif actions[action] == 'down' and current_y < maze.y_size - 1:
        new_y += 1
    elif actions[action] == 'right' and current_x < maze.x_size - 1:
        new_x += 1
    elif actions[action] == 'left' and current_x > 0:
        new_x -= 1

    return new_x, new_y


def get_shortest_path(start_x, start_y, maze):
    # Find path from (start_x, start_y) to Destination using the Q values.
    final_path = []
    if is_terminal_state(start_x, start_y, maze):
        return []

    else:
        current_x, current_y = start_x, start_y
        shortest_path = []
        shortest_path.append([current_x, current_y])
        n = 0
        
        while not is_terminal_state(current_x, current_y, maze):
            if n > 1000:
                print('Path not found')
                return []
            action = get_next_action(current_x, current_y, 1, maze.q_values)
            current_x, current_y = get_next_location(
                current_x, current_y, action, maze)
            shortest_path.append([current_x, current_y])
            n += 1
        if shortest_path[-1] == maze.destination:
            print('Start ->')
            for step in shortest_path:
                print('({}, {})'.format(step[0], step[1]), end=' -> ')
            print('End')
        else:
            print('Path not found')
        return shortest_path


def get_starting_location(maze):
    # returns random location at the beginning of episode.
    current_x = np.random.randint(maze.x_size)
    current_y = np.random.randint(maze.y_size)

    while is_terminal_state(current_x, current_y, maze):
        current_x = np.random.randint(maze.x_size)
        current_y = np.random.randint(maze.y_size)

    return current_x, current_y
