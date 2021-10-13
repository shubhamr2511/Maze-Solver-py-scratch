import numpy as np
import maze_utils as util

def random(maze, wall_density=0.5):
    wall_density = min(1,wall_density)
    for x in range(maze.x_size):
        for y in range(maze.y_size):
            if [x,y] != maze.destination:
                if np.random.random() < wall_density:
                    util.add_wall(x,y,maze)

# TODO
def recursive_division(maze):
    # not complete
    xl = 1
    yl = 1
    xh = maze.x_size-1
    yh = maze.y_size-1
    n = 3

    def subdivide(xl, xh, yl, yh, maze):
        if xh-xl <= 3 or yh-yl<=3:
            return
        
        px = np.random.randint(xl,xh)
        util.remove_wall(px, yh, maze)
        py = np.random.randint(yl,yh)
        util.remove_wall(xh, py, maze)

        x = np.random.randint(xl+1, xh-1)
        y = np.random.randint(yl+1, yh-1)
        print('passage:',px,py)
        if x!=px:
            for i in range(yl, yh):
                util.add_wall(x,i, maze)
        if y!=py:
            for i in range(xl, xh):
                util.add_wall(i,y, maze)
        print('wall:',x,y)
        maze.edit()
        subdivide(xl, x, yl, y, maze)
        subdivide(x, xh, yl, y, maze)
        subdivide(xl, x, y, yh, maze)
        subdivide(x, xh, y, yh, maze)

    subdivide(xl,xh, yl, yh, maze)
    # maze generation algorithms
