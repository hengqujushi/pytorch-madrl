
from DQN import DQN

import sys
import gym
import numpy as np
import matplotlib.pyplot as plt


MAX_EPISODES = 10000
EPISODES_BEFORE_TRAIN = 20
EVAL_EPISODES = 10
EVAL_INTERVAL = 20
# max steps in each episode
MAX_STEPS = 10000

MEMORY_CAPACITY = 10000
BATCH_SIZE = 1000
LOSS_TYPE = "mse"
MAX_GRAD_NORM = None

REWARD_DISCOUNTED_GAMMA = 0.999

EPSILON_START = 0.99
EPSILON_END = 0.05
EPSILON_DECAY = 500

DONE_PENALTY = -10.

RANDOM_SEED = 2017


def run(env_id="CartPole-v0"):

    env = gym.make(env_id)
    env.seed(RANDOM_SEED)
    env_eval = gym.make(env_id)
    env_eval.seed(RANDOM_SEED)
    state_dim = env.observation_space.shape[0]
    if len(env.action_space.shape) > 1:
        action_dim = env.action_space.shape[0]
    else:
        action_dim = env.action_space.n

    dqn = DQN(env=env, memory_capacity=MEMORY_CAPACITY,
              state_dim=state_dim, action_dim=action_dim,
              batch_size=BATCH_SIZE, max_steps=MAX_STEPS,
              done_penalty=DONE_PENALTY, loss=LOSS_TYPE,
              reward_gamma=REWARD_DISCOUNTED_GAMMA,
              epsilon_start=EPSILON_START, epsilon_end=EPSILON_END,
              epsilon_decay=EPSILON_DECAY, max_grad_norm=MAX_GRAD_NORM,
              episodes_before_train=EPISODES_BEFORE_TRAIN)

    episodes =[]
    eval_rewards =[]
    while dqn.n_episodes < MAX_EPISODES:
        dqn.interact()
        if dqn.n_episodes >= EPISODES_BEFORE_TRAIN:
            dqn.train()
        if dqn.episode_done and ((dqn.n_episodes+1)%EVAL_INTERVAL == 0):
            rewards = dqn.evaluation(env_eval, EVAL_EPISODES)
            print("Episode %d, Average Reward %.2f" % (dqn.n_episodes+1, rewards))
            episodes.append(dqn.n_episodes+1)
            eval_rewards.append(rewards)

    episodes = np.array(episodes)
    eval_rewards = np.array(eval_rewards)
    np.savetxt("./output/%s_dqn_episodes.txt"%env_id, episodes)
    np.savetxt("./output/%s_dqn_eval_rewards.txt"%env_id, eval_rewards)

    plt.figure()
    plt.plot(episodes, eval_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Average Reward")
    plt.legend(["DQN"])
    plt.savefig("./output/%s_dqn.png"%env_id)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run(sys.argv[1])
    else:
        run()