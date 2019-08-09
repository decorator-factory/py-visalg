

from visalg import AlgImage, ImageFont, Grid, ColorFill

img = AlgImage(480, 280)

grid = Grid(x=16, y=16,
            width=13, height=7,
            font=None,
            margin=3,
            cell_size=32,
            intercell_space=0,
            outline="#444444")

img << grid

"""
ColorFill fills a cell with a predefined color instead
of displaying a character in it.
If you put "red" into a cell, it will display the text "red".
If you put ColorFill("red") into a cell, no text will be displayed in the cell,
but it will be filled with color red.
"""

BLACK = ColorFill("#000000")
WHITE = ColorFill("#ffffff")
RED = ColorFill("#ff0000")
YELLOW = ColorFill("yellow")


maze = ("$$$$$$$$$$$$$",
        "$X       $  $",
        "$$$$$$ $$$$ $",
        "$   G$      $",
        "$ $$$$ $$$$ $",
        "$         $ $",
        "$$$$$$$$$$$$$")

HEIGHT = len(maze)
WIDTH = len(maze[0])

robot_x, robot_y = 0, 0 # robot position
goal_x, goal_y = 0, 0 # goal position

for x in range(WIDTH):
    for y in range(HEIGHT):
        v = maze[y][x]

        grid[x, y] = {
                        "$": BLACK,
                        "X": RED,
                        "G": YELLOW,
                        " ": WHITE
                    }[v]

        if v == "X":
            robot_x, robot_y = x, y

        if v == "G":
            goal_x, goal_y = x, y

# (dx, dy) is a vector of length 1
# That determines where the robot is looking


"""
The maze solving algorithm:

solve_maze(){
    rotate_ccw;
    if (forward_is_free){
    	forward;
    }else{
    	u_turn;
    	solve_maze();
    }
}
"""

def rotate_ccw(dx, dy):
    return dy, -dx

def uturn(dx, dy):
    return -dx, -dy

dx, dy = (1, 0)

def solve_maze():
    global dx, dy, robot_x, robot_y,\
           goal_x, goal_y, img, grid

    if (robot_x, robot_y) == (goal_x, goal_y):
        return

    img.capture()

    dx, dy = rotate_ccw(dx, dy)
    next_x, next_y = robot_x + dx, robot_y + dy


    # Highlight one cell:
    grid.highlight["#0000ff"] = [(next_x, next_y)]
    img.capture()

    # if the next position is empty
    if grid[next_x, next_y] in (WHITE, YELLOW):
        img.capture()
        img.capture()
        # Fill the old position with white color
        grid[robot_x, robot_y] = WHITE
        robot_x, robot_y = next_x, next_y

        # Fill the new position with red color
        grid[robot_x, robot_y] = RED

        img.capture()
    else:
        dx, dy = uturn(dx, dy)

    solve_maze()

solve_maze()

[img.capture() for _ in range(8)]
img.save_gif("examples/maze.gif", duration=100)

del img