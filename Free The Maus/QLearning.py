import time
import random

from QTable import QTable
from Types import Action, Rewards
from MazeEnvironment import MazeEnvironment

if __name__ == "__main__":

    # Training parameters
    MaxEpisodes = 100
    MaxStepsPerEpisode = 100

    # Hyperparameters
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1

    # Setup reward function
    rewards = Rewards(
        Goal=5,
        SideGoal=1,
        Trap=-5,
        TimeStep=-0.1,
        # NotAValidMove=-0.001
    )

    # Setup Environment
    maze_file = "maze_10x10.txt"

    env = MazeEnvironment(maze_file, rewards)

    # Setup Q-Table
    q_table = QTable(actions=len(Action))

    # Time the training
    t0 = time.time()

    # Run training
    for i in range(MaxEpisodes):
        # Reset episode
        done = False
        state = env.reset()

        # Run training episode
        for s in range(MaxStepsPerEpisode):
            # Explore the environment / Chose random action
            if random.uniform(0, 1) < epsilon:
                action = random.choice(list(Action))

            else:  # Exploit learned values
                action = Action(q_table.get_max_q_value(state))

            # Take action
            next_state, reward, done = env.step(action)

            # Update Q-table
            old_value = q_table.get_q_values(state)[action.value]
            next_max = max(q_table.get_q_values(next_state))

            new_value = (1 - alpha) * old_value + alpha * \
                (reward + gamma * next_max)

            q_table.update_q_value(
                state, action=action.value, new_value=new_value)

            # Check if episode was terminated
            if done:
                break

            # Update current state
            state = next_state

        if i % 10 == 0:  # Log progress
            print(f"Episode: {i}")

    t1 = time.time()

    print(f"Time: {t1-t0:.2f}s")

    print("Training finished.")

    # Test the trained Q-table
    state = env.reset()
    env.render()

    for i in range(MaxStepsPerEpisode):
        # Follow a greedy policy when testing
        action = Action(q_table.get_max_q_value(state))
        state, reward, done = env.step(action)

        print(f"Step {i}: Go {action.name}, {reward =}")

        # Update maze
        env.render()

        # End Episode
        if done:
            break

    # Stop program from exiting
    input()
