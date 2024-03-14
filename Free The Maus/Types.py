from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, TypeAlias

"""Type alias for a maze state."""
Maze: TypeAlias = List[List[int]]

"""Type alias for a colored maze image."""
ColoredMaze: TypeAlias = List[List[Tuple[int, int, int]]]

"""Mapping between a maze state and a color."""
MazeColorMap = {
    0: (255, 255, 255),    # white, Empty
    1: (0, 0, 0),          # black, Wall
    2: (0, 0, 255),        # blue, Current Pose
    3: (0, 255, 0),        # green, Goal Pose
    4: (255, 255, 0),      # yellow, Side Goal
    5: (255, 0, 0)         # red, Trap
}


class Action(Enum):
    """Enum for all possible actions."""

    Up = 0
    Down = 1
    Left = 2
    Right = 3


class MazeStates(Enum):
    """Enum for all Maze states."""

    Empty = 0
    Wall = 1
    MyPosition = 2
    Goal = 3
    SideGoal = 4
    Trap = 5


@dataclass
class Rewards:
    """Dataclass with all the weights for the reward function."""

    Goal: float
    SideGoal: float
    Trap: float
    TimeStep: float = 0
    NotAValidMove: float = 0
