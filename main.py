from dqn_agent import DQNAgent
from gym_core import tgym
import numpy as np


def edit_state(s1, s2, s3):
    state = list()
    for value in s1.values:
        state.append(value)
    for value in s2.values:
        state.append(value)
    for value in s3:
        state.append(value)

    state = np.array(state)
    return state


if __name__ == '__main__':
    EPISODES = 10000
    RENDER = False
    ACTION_SIZE = 2

    env = tgym.TradingGymEnv(episode_type='0', percent_goal_profit=10, percent_stop_loss=1)
    s1, s2, s3 = env.init_observation()  # to calculate length of state data
    state = edit_state(s1, s2, s3)
    agent = DQNAgent.DQNAgent(state_size=len(state), action_size=ACTION_SIZE)

    for ep in range(EPISODES):
        score = 0
        done = False
        env.reset()
        s1, s2, s3 = env.init_observation()
        state = edit_state(s1, s2, s3)

        r0 = 0
        r1 = 0
        r2 = 0
        while not done:
            if RENDER:
                env.render()
            action = agent.get_action(state)
            next_state, _, done, info = env.step(action)
            # print(info)
            next_state = edit_state(next_state[0], next_state[1], next_state[2])
            reward = agent.calc_reward(info, action)
            if reward == 0:
                r0 += 1
            if reward == -1:
                r1 += 1
            if reward == 1:
                r2 += 1
            agent.append_sample(state, action, reward, next_state, done)
            if len(agent.memory) >= agent.train_start:
                agent.train_model()
                # print(action, reward)

            state = next_state
            score += reward

            if done:
                print(r0, r1, r2)
                agent.update_target_model()
                agent.save_model()
                print('profit :', score, 'memory :', len(agent.memory), 'epsilon :', round(agent.epsilon, 5))
                break

