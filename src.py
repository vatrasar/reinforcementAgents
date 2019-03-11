from typing import List
from agentQL import Agent
import pygame
from block import Block
from config import config
import pickle
import random
from time import time


class Game:
    def __init__(self,display):
        self.display=display

    def loop(self):

        episode=0
        start_time = time()
        agent=self.load_form_file()
        while True:
            clock = pygame.time.Clock()
            elements_list: List[Block]=self.build_elements_list()
            hero=elements_list[len(elements_list)-2]

            score=0

            episode+=1

            while True:
                self.display.fill(config['colors']['black'])
                action,old_state = agent.get_action(elements_list)
                self.agent_step(action, elements_list, hero)
                drawn_elements_list = self.draw_elements(elements_list)
                if time()-start_time>60:
                    print("SAVEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
                    start_time = self.save_to_file(agent, start_time)

                #result if die
                if not(self.is_hero_alive(drawn_elements_list)) or score<-200:
                    reward=-100
                    score+=reward
                    agent.upload_results(reward,action,old_state,elements_list)
                    # print("Przegrana score:"+str(score))
                    break
                #result if win o
                if self.is_win(drawn_elements_list):
                    reward = 100
                    score += reward
                    agent.upload_results(reward,  action, old_state,elements_list)
                    agent.decrease_exploration_ratio()
                    # if episode%1000>900:
                    print("Wygrana score:"+str(score)+"\nepisode:"+str(episode))

                    break
                #result if not win or die
                reward = -1
                score += reward
                agent.upload_results(reward,action, old_state,elements_list)


                clock.tick(config["game"]["fps"])
                pygame.display.update()

    def save_to_file(self, agent, start_time):
        # save
        binary_file = open('my_pickled_mary.bin', mode='wb')
        my_pickled_mary = pickle.dump(agent, binary_file)
        binary_file.close()
        start_time = time()

        return start_time

    def agent_step(self,action, elements_list, hero):

        if action == 0:
            if hero.position[1] - config["game"]["block_size"] > 0:
                hero.position[1] -= config["game"]["block_size"]
        if action == 1:
            if hero.position[1] + config["game"]["block_size"] < config["game"]["width"] - config["game"][
                "block_size"]:
                hero.position[1] += config["game"]["block_size"]
        if action == 2:
            if hero.position[0] + config["game"]["block_size"] < config["game"]["height"] - config["game"][
                "block_size"]:
                hero.position[0] += config["game"]["block_size"]
        if action == 3:
            if hero.position[0] - config["game"]["block_size"] > 0:
                hero.position[0] -= config["game"]["block_size"]

    def human_step(self, hero):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if hero.position[1] - config["game"]["block_size"] > 0:
                        hero.position[1] -= config["game"]["block_size"]
                if event.key == pygame.K_DOWN:
                    if hero.position[1] + config["game"]["block_size"] < config["game"]["width"] - config["game"][
                        "block_size"]:
                        hero.position[1] += config["game"]["block_size"]
                if event.key == pygame.K_RIGHT:
                    if hero.position[0] + config["game"]["block_size"] < config["game"]["height"] - config["game"][
                        "block_size"]:
                        hero.position[0] += config["game"]["block_size"]
                if event.key == pygame.K_LEFT:
                    if hero.position[0] - config["game"]["block_size"] > 0:
                        hero.position[0] -= config["game"]["block_size"]

    def is_hero_alive(self, drawn_elements_list):
        hero = drawn_elements_list[len(drawn_elements_list) - 2]
        target = drawn_elements_list[len(drawn_elements_list) - 1]
        guards = drawn_elements_list[0:len(drawn_elements_list) - 2]
        for guardian in guards:
            if guardian.colliderect(hero):
                return False
        return True

    def is_win(self, drawn_elements_list):
        hero = drawn_elements_list[len(drawn_elements_list) - 2]
        target = drawn_elements_list[len(drawn_elements_list) - 1]
        return hero.colliderect(target)

    def build_elements_list(self):
        elements_list=self.build_guard()
        elements_list.append(self.build_element(elements_list,config["hero"]))
        elements_list.append(self.build_element(elements_list,config["target"]))
        return elements_list


    def build_guard(self):
        guard = list()
        for i in range(0, config["enemy_number"]):

            new_guardian=Block(config["enemy"], self.get_random_position())
            while not(self.validate_position(guard, new_guardian)):
                new_guardian = Block(config["enemy"], self.get_random_position())
            guard.append(new_guardian)

        return guard

    def get_random_position(self):
        valid_x=range(int(config["game"]["block_size"]/2),config["game"]["width"]-int(config["game"]["block_size"]/2),config["game"]["block_size"])
        valid_y=range(int(config["game"]["block_size"]/2),config["game"]["height"]-int(config["game"]["block_size"]/2),config["game"]["block_size"])
        return [valid_x[random.randint(0,len(valid_x)-1)],valid_y[random.randint(0,len(valid_y)-1)]]
        # return [random.randint(config["game"]["block_size"], config["game"]["width"] - config["game"]["block_size"]),
        #  random.randint(config["game"]["block_size"], config["game"]["height"] - config["game"]["block_size"])]
    def validate_position(self, block_set: list, new_block):

       for block in block_set:
           if new_block==block:
                return False

       return True

    def build_element(self,elements_list,element_name):
        new_hero = Block(element_name, self.get_random_position())
        while not(self.validate_position(elements_list, new_hero)):
            new_hero = Block(element_name, self.get_random_position())
        return new_hero

    def draw_elements(self, elements_list):
        drawn_elements_list=list()
        element: Block
        for element in elements_list:
            drawn_elements_list.append(element.draw(self.display))
        return drawn_elements_list

    def load_form_file(self):
        open_file = open('my_pickled_mary.bin', mode='rb')

        model = pickle.load(open_file)
        open_file.close()
        return model





