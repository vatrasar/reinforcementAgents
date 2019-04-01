from block import Block
from config import config
from src import Game
from agentQN import AgentQN
from block import Block
import numpy as np
def test_eq():
    bloczek1=Block("enemy",[40,40])
    bloczek2=Block("enemy",[40,40])
    assert bloczek1==bloczek2
    bloczek1 = Block("enemy", [40, 80])
    bloczek2 = Block("enemy", [40, 40])
    assert not(bloczek1 == bloczek2)
    bloczek1 = Block("enemy", [40, 50])
    bloczek2 = Block("enemy", [40, 40])
    assert bloczek1 == bloczek2
    bloczek1 = Block("enemy", [80, 40])
    bloczek2 = Block("enemy", [40, 40])
    assert not(bloczek1 == bloczek2)
    bloczek1 = Block("enemy", [80, 40])
    bloczek2 = Block("enemy", [40, 80])
    assert not (bloczek1 == bloczek2)
def test_valid():
    game=Game((1))
    block_list=[Block("enemy", [80, 40]),Block("enemy", [40, 40])]
    new_block= Block("enemy", [120, 120])
    assert game.validate_position(block_list,new_block)
    new_block = Block("enemy", [70, 40])
    assert not(game.validate_position(block_list, new_block))

def test_convert_to_state():
    state=[Block(config["enemy"],[1,1]),Block(config["enemy"],[4,9]),Block(config["hero"],[9,9])]
    agent=AgentQN()
    result=agent.convert_to_state(state)
    test=np.array([1,1,1,4,9,1,9,9,2])
    assert np.array_equal(result,test)
