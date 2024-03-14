import os
import copy

import matplotlib.pyplot as plt

from typing import Tuple

from Types import Action, Maze, MazeStates, Rewards
from MazeUtilities import load_maze, make_colored_maze, plot_maze


class MazeEnvironment:
    def __init__(self, maze_file: str | os.PathLike,
                 rewards: Rewards) -> None:
        """Environment that holds a maze where a virtual mouse can navigate, eat cheese, 
            get trapped and leave the maze.

            Reaching the exit, or getting trapped will result in immediate termination 
            of the episode.

        Note: With the current implementation all side goals could only be used once.

        Maze file example:
            0, 2, 1, 1, 0;
            0, 1, 1, 0, 0;
            1, 1, 0, 3, 0;
            1, 0, 5, 4, 1;
            0, 0, 0, 1, 1;

            Each number represents whether the position is occupied or not.
                    0: Empty position.
                    1: Wall, position can never be occupied.
                    2: My (the mouse's) position.
                    3: Goal position, maze exit, reaching this position will lead to a terminating state
                    4: Side goal, piece of cheese.
                    5: Trap, reaching this position will lead to a terminating state.

        Args:
            maze_file (str | os.PathLike): Text file describing the maze.
            rewards (Rewards): Weights to be used by the reward function.
        """

        self._maze_file = maze_file
        self._rewards = rewards

        self._figax = None

    @property
    def current_maze(self) -> Maze:
        """Returns the current maze state."""

        # Use a deep copy of the maze for external use!
        # Other wise any change to one instance will affect the other.
        return copy.deepcopy(self._current_maze)

    @property
    def maze_shape(self) -> Tuple[int, int]:
        """Returns the maze's shape."""

        return len(self._current_maze[0]), len(self._current_maze)

    @property
    def _current_position(self) -> Tuple[int, int]:
        """Finds and returns the position of the mouse in the maze.

        Returns:
            Tuple[int, int]: Position.
        """

        for y in range(self.maze_shape[1]):
            for x in range(self.maze_shape[0]):
                if self._current_maze[y][x] == MazeStates.MyPosition.value:
                    return (x, y)

        # The mouse wasn't found!
        raise Exception(
            "Agent couldn't be found! Did you change the mazes state?"
        )

    def get_offset_from_action(self, action: Action) -> Tuple[int, int]:
        """Map an action into a position offset for the maze.

        Args:
            action (Action): Action to be used.

        Returns:
            Tuple[int, int]: Position offset for the chosen action.
        """

        if action == Action.Up:
            return 0, -1

        if action == Action.Down:
            return 0, 1

        if action == Action.Right:
            return 1, 0

        if action == Action.Left:
            return -1, 0

        # Action is not recognized
        raise NotImplementedError(f"Action {action} not supported!")

    def _get_reward(self, position: Tuple[int, int]) -> Tuple[float, bool]:
        """Get the reward for the given position. 
        Also checks if the we have reached a terminating state.

        Args:
            position (Tuple[int, int]): Position to be used for the reward calculation.

        Returns:
            Tuple[float, bool]: Reward, done.
        """

        current_state = MazeStates(
            self._current_maze[position[1]][position[0]])

        if current_state == MazeStates.Goal:
            return self._rewards.Goal, True

        if current_state == MazeStates.SideGoal:
            return self._rewards.SideGoal, False

        if current_state == MazeStates.Trap:
            return self._rewards.Trap, True

        return self._rewards.TimeStep, False

    def _get_did_update_reward(self, did_update: bool) -> float:
        """Extra reward function used for a unsuccessful update of the maze.

        Args:
            did_update (bool): Whether the lasst action resulted in tha maze to be updated or not.

        Returns:
            float: Reward.
        """

        if not did_update:
            return self._rewards.NotAValidMove

        return 0

    def _update_position(self, new_position: Tuple[int, int]) -> bool:
        """Update the agents position.

        Args:
            new_position (Tuple[int, int]): New position.

        Returns:
            bool: Whether the new position was valid and successfully updated.
        """

        old_position = self._current_position

        if self._current_maze[new_position[1]][new_position[0]] == MazeStates.Wall.value:
            # Ignore action if wall
            return False

        if ((old_position[0] == new_position[0]) and old_position[1] == new_position[1]):
            # Same position
            return False

        self._current_maze[old_position[1]
                           ][old_position[0]] = MazeStates.Empty.value

        self._current_maze[new_position[1]][new_position[0]
                                            ] = MazeStates.MyPosition.value

        return True

    def step(self, action: Action) -> Tuple[Maze, float, bool]:
        """Take an action.

        Args:
            action (Action): Chosen action.

        Returns:
            Tuple[Maze, float, bool]: State, reward, done.
        """

        # Map action to an offset
        offset = self.get_offset_from_action(action)

        # Update position
        current_position = self._current_position

        new_position = (
            max(min(current_position[0] + offset[0], len(self._current_maze[0])-1), 0
                ),
            max(min(current_position[1] + offset[1],
                len(self._current_maze)-1), 0),

        )

        # Get reward and update the internal state
        reward, done = self._get_reward(position=new_position)

        did_update = self._update_position(new_position)

        # Add reward for whether the position was updated or not
        # This wasn't added added to the get_reward function, because it must be
        # called before the update_position function.
        reward += self._get_did_update_reward(did_update=did_update)

        return self.current_maze, reward, done

    def reset(self) -> Maze:
        """Reset environment.

        Returns:
            Maze: State.
        """

        # Reset maze
        self._current_maze = load_maze(file=self._maze_file)

        # Close open figures
        if self._figax is not None:
            plt.close(self._figax[0])

        self._figax = None

        return self.current_maze

    def render(self):
        """Render maze."""

        colored_maze = make_colored_maze(
            maze=self._current_maze)
        self._figax = plot_maze(colored_maze, figax=self._figax)


if __name__ == "__main__":

    # Test the environment

    # Setup the Environment
    maze_file = "maze_10x10.txt"

    rewards = Rewards(
        Goal=5,
        SideGoal=1,
        Trap=-5,
    )

    max_steps = 25

    env = MazeEnvironment(maze_file, rewards)

    # Manually chosen Actions
    actions = [
        Action.Down, Action.Right, Action.Right,
        Action.Right, Action.Down, Action.Down,
        Action.Right, Action.Right, Action.Right,
        Action.Down, Action.Down, Action.Right,
        Action.Down, Action.Down, Action.Down,
        Action.Down, Action.Right, Action.Right,
        Action.Down
    ]

    # Rest Environment
    state = env.reset()
    env.render()

    # Execute the actions in the Environment
    for i in range(max_steps):
        state, reward, done = env.step(actions[i])
        print(f"i: {i} {reward=} {done=}")

        env.render()

        if done:
            break
