import random
import numpy as np
from config import config
import tensorflow as tf
from block import Block
import typing

class AgentQN:


    def __init__(self):
        tf.reset_default_graph()
        self.actions=range(0,4)
        #Qnetwrk initialization
        self.inputs1 = tf.placeholder(shape=[1, 3 * (config["enemy_number"] + 2)], dtype=tf.float32)
        self.W = tf.Variable(tf.random_uniform([3 * (config["enemy_number"] + 2), 4], 0, 0.01))
        self.Qout = tf.matmul(self.inputs1,self.W)
        self.predict = tf.argmax(self.Qout, 1)
        self.exploration_rate=0.1
        self.learning_rate = 0.1  # Learning rate
        self.gamma = .99  # Discounting rate
        self.nextQ = tf.placeholder(shape=[1, 4], dtype=tf.float32)

        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Qout))
        self.trainer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate)
        self.updateModel = self.trainer.minimize(self.loss)
        init = tf.initialize_all_variables()

        self.sess = tf.Session()
        self.sess.run(init)


    def get_action(self, elements_list):
        state=self.convert_to_state(elements_list)
        if self.exploration_rate<np.random.rand(1):
            a= self.sess.run(self.predict, feed_dict={self.inputs1: state})

            return (self.actions[a[0]],state)

        else:
            return (random.randint(0,3),state)



    def convert_to_state(self, elements_list: typing.List[Block]) -> np.ndarray:
        state_list=[]
        map_shape=()
        state=np.array(np.zeros([config]))
        elements_types = {config["enemy"]:1,config["hero"]:2,config["target"]:3}
        for element in elements_list:
            state_list.append(element.position[0])
            state_list.append(element.position[1])
            state_list.append(elements_types[element.name])
        state_array=np.asarray(state_list,np.int32)
        return state_array.reshape((1,state_array.shape[0]))



    def upload_results(self, reward, action, old_state,new_elements_list):
        """

        attention! action have to be a number!
        """

        new_state = self.convert_to_state(new_elements_list)
        new_q_values = self.sess.run(self.Qout, feed_dict={self.inputs1: new_state})
        old_q_values = self.sess.run(self.Qout, feed_dict={self.inputs1: old_state})
        max_q_value = np.max(new_q_values)
        old_q_values[0, action] = reward + self.gamma * max_q_value

        _, W = self.sess.run([self.updateModel, self.W], feed_dict={self.inputs1: old_state, self.nextQ: old_q_values})


    def decrease_exploration_ratio(self,episode_num):

        self.exploration_rate=1./((episode_num / 50) + 10)