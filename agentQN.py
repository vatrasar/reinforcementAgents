import random
import numpy as np
from config import config
import tensorflow as tf
from block import Block
import typing

class AgentQN:
    def __init__(self):
        self.actions=range(0,4)
        #Qnetwrk initialization
        inputs1 = tf.placeholder(shape=[1, 16], dtype=tf.float32)
        W = tf.Variable(tf.random_uniform([16, 4], 0, 0.01))
        Qout = tf.matmul(inputs1, W)
        predict = tf.argmax(Qout, 1)
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


    def convert_to_state(self, elements_list: typing.List[Block]):
        state_list=[]
        elements_types = {config["enemy"]:1,config["hero"]:2,config["target"]:3}
        for element in elements_list:
            state_list.append(element.position[0])
            state_list.append(element.position[1])
            state_list.append(elements_types[element.name])
        return np.asarray(state_list,np.int32)


    def upload_results(self, reward, action, old_state,new_elements_list):
        new_state=self.convert_to_state(new_elements_list)

        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        self.q_table[old_state][action] = self.q_table[old_state][action] + self.learning_rate * (reward + self.gamma *
                                                                     np.max(self.q_table.get(new_state,np.zeros(config["game"]["action_size"]))) - self.q_table[old_state][action])

    def decrease_exploration_ratio(self):
        if self.exploration_rate>0.01:
         self.exploration_rate-=0.1