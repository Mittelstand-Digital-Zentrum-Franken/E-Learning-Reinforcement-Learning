import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt

from os import PathLike
from typing import Optional, Tuple

from Types import Maze, MazeColorMap, ColoredMaze


def load_maze(file: str | PathLike) -> Maze:
    """Load a maze from text file.

    Example on how to format maze:
    0, 2, 1, 1, 0;
    0, 1, 1, 0, 0;
    1, 1, 0, 3, 0;
    1, 0, 5, 4, 1;
    0, 0, 0, 1, 1;

    Args:
        file (str | PathLike): Path to file.

    Returns:
        Maze: Loaded maze.
    """

    with open(file) as f:
        maze_raw = f.read()
        maze = [
            [
                int(column.strip())
                for column in row.split(",")
            ]
            for row in maze_raw.split(";") if row.strip() != ""
        ]

        return maze


def make_colored_maze(maze: Maze,
                      ) -> ColoredMaze:
    """Map maze states to colors given the color map.

    Args:
        maze (Maze): Maze to be used.

    Returns:
        ColoredMaze: Colored maze.
    """

    return [
        [MazeColorMap[column] for column in row]
        for row in maze
    ]


def plot_maze(colored_maze: ColoredMaze,
              figsize: Tuple[int, int] = (5, 5),
              figax: Optional[Tuple[matplotlib.figure.Figure,
                                    matplotlib.axes.Axes]] = None,
              wait: float = 1
              ) -> Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]:
    """Plot the maze.

    Args:
        colored_maze (ColoredMaze): Colored maze.
        figsize (Tuple[int, int], optional): Figure size. Defaults to (5,5).
        figax (Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]], 
                    optional): Figure and axes to be updated. If none is given, new ones will be created. Defaults to None.
        wait (float, optional): How much to wait or block the code after updating the mazes plot. 
            If -1 is given, plt.show will be used und the code will wait indefinitely. Defaults to 1.

    Returns:
        Optional[Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]]: Reference to the figure and axes.
    """

    if figax is None:
        fig, ax = plt.subplots(figsize=figsize)

        # Set the border color to black
        fig.patch.set_edgecolor('black')
        fig.patch.set_linewidth(0.2)

        # Make maze grid
        ax.set_xticks([i - 0.5 for i in range(len(colored_maze[0]))])
        ax.set_yticks([i - 0.5 for i in range(len(colored_maze))])

        # Clear ticks label
        ax.get_xaxis().set_ticklabels([])
        ax.get_yaxis().set_ticklabels([])

        # Show grid
        ax.grid()

    else:
        fig, ax = figax

    # Plot maze as an colored image
    ax.imshow(colored_maze, interpolation='nearest')

    if wait == -1:  # Block code from continuing
        plt.show()

    else:  # Wait for update
        plt.pause(wait)

    return fig, ax


if __name__ == "__main__":
    # Test the utility functions

    maze_file = "maze_10x10.txt"

    # Load Maze
    maze = load_maze(file=maze_file)

    # Map Colors
    colored_maze = make_colored_maze(maze)

    # Plot Maze
    plot_maze(colored_maze, wait=-1)
