import random
import numpy as np
from config import config

class Agent:
    def __init__(self):
        self.actions=range(0,4)
        self.q_table={}
        self.exploration_rate=0.01
        self.learning_rate = 0.7  # Learning rate
        self.gamma = 0.618  # Discounting rate

    def get_action(self, elements_list):
        state=self.convert_to_state(elements_list)
        if self.exploration_rate<random.uniform(0,1):
            if state in self.q_table.keys():
                return (self.actions[int(np.argmax(self.q_table[state]))],state)
            else:
                self.q_table[state]=np.zeros(config["game"]["action_size"])
                return (random.randint(0,3),state)
        else:
            if state not in self.q_table.keys():
                self.q_table[state] = np.zeros(config["game"]["action_size"])
            return (random.randint(0,3),state)


    def convert_to_state(self, elements_list):
        return tuple(map(lambda element:tuple(element.position),elements_list))

    def upload_results(self, reward, action, old_state,new_elements_list):
        new_state=self.convert_to_state(new_elements_list)

        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        self.q_table[old_state][action] = self.q_table[old_state][action] + self.learning_rate * (reward + self.gamma *
                                                                     np.max(self.q_table.get(new_state,np.zeros(config["game"]["action_size"]))) - self.q_table[old_state][action])

    def decrease_exploration_ratio(self):
        if self.exploration_rate>0.01:
         self.exploration_rate-=0.1



