from typing import List

from Types import Maze


class QTable:
    def __init__(self, actions: int):
        """Makes and manages a Q-Table. The states are tailored to fit the maze.

        Args:
            actions (int): Number of possible actions.
        """

        self._states = {}
        self._vales = {}

        self._actions = actions

    def _are_states_equal(self, state1: Maze, state2: Maze) -> bool:
        """Check if two states are the same.

        Args:
            state1 (Maze): First state.
            state2 (Maze): Second state.

        Returns:
            bool: Whether or not the states are equal.
        """

        if len(state1) != len(state2):
            return False

        for stt1, stt2 in zip(state1, state2):
            if len(stt1) != len(stt2):
                return False

            for s1, s2 in zip(stt1, stt2):
                if s1 != s2:
                    return False

        return True

    def _add_state(self, state: List[List[int]]) -> List[float]:
        """Add a new state to the Q-table.

        Args:
            state (List[List[int]]): State to be added.

        Returns:
            List[float]: List of Q-values assigned to the state.
        """

        idx = 0 if len(self._states) == 0 else max(self._states.keys()) + 1

        self._states[idx] = state
        self._vales[idx] = [0]*self._actions

        return self._vales[idx]

    def get_q_values(self, state: Maze) -> List[float]:
        """Get the list of Q-values for a given state.

        Args:
            state (Maze): State to be used.

        Returns:
            List[float]: List of Q-values.
        """

        for idx, s in self._states.items():
            if self._are_states_equal(s, state):
                return self._vales[idx]

        # State is not yet known, add it
        return self._add_state(state)

    def get_max_q_value(self, state: Maze) -> int:
        """Get the action index with the highest Q-value for the given state.

        Note: The current implementation will always return the first action
              with highest value. If two or more actions have the same value, 
              you could add some randomness and flip a coin before choosing which.

        Args:
            state (Maze): State to be used.

        Returns:
            int: Action index with the highest Q-value. 
        """

        values = self.get_q_values(state)

        return values.index(max(values))

    def update_q_value(self, state: Maze, action: int, new_value: float):
        """Update a Q-value.

        Args:
            state (Maze): State to be used.
            action (_type_): Index of action for which to update the Q-value.
            new_value (float): New Q-value. 
        """

        for idx, s in self._states.items():
            if self._are_states_equal(s, state):
                self._vales[idx][action] = new_value
                return

        raise Exception("Unknown state was given!")


if __name__ == "__main__":
    # Test the Q-Table class

    q_table = QTable(actions=6)

    # Test adding a new state
    state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

    q_table._add_state(state)
    print(q_table.get_q_values(state))

    # Test updating a value
    q_table.update_q_value(state, action=2, new_value=3)
    print(q_table.get_q_values(state))

    # Test getting a values from unknown state
    state2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 12, 10, 12], [13, 14, 15, 16]]
    print(q_table.get_q_values(state2))
