# run on python 3.8 (gym doesnt run on 3.9 python)
# pip install tensorflow
# pip install gym
# pip install keras
# pip install keras-rl2(RL2)
# make sure you're using the right python interpreter
# ctrl+shift+p
# Python: Select Interpreter
# Python 3.8
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.models import Sequential
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
import tkinter as tk
import random
import sys
sys.path.append(
    'C:\\users\\01bba\\appdata\\local\\programs\\python\\python38\\lib\\site-packages') # pip show gym and put replace with path


class TrafficEnv(Env):
    def __init__(self):
        self.numlanes = 5
        self.leftlanes = 2
        self.queuesize = 5
        self.initial_time = 60
        self.lanes = np.zeros((self.numlanes, self.queuesize), dtype=int)
        # possible actions
        # 0 ns left turn
        # 1 ns straight
        # 2 we left turn
        # 3 we straight
        self.action_space = Discrete(4)
        # dont know if this is right to put as an observation space
        self.observation_space = self.lanes
        # self.state
        for r in range(self.numlanes):
            for c in range(self.queuesize):
                self.lanes[r, c] = random.randint(0, self.queuesize)
        self.state = self.lanes
        # defined time length
        self.time_length = self.initial_time

    def steps(self, action):
        self.state = self.runAction(action)
        self.time_length -= 1
        # calculate sum of cars
        for r in self.lanes:
            for c in self.lanes[r]:
                self.sum = self.lanes[r, c]

        # calculate reward
        reward = 0
        if self.sum == 0:
            reward += 1
        else:
            reward += -.5*self.sum

        # check if time is over
        if self.time_length <= 0:
            done = True
        else:
            done = False

        # add randomness? stochasticity

        # placeholder for step information
        info = {}

        return self.state, reward, done, info

    def runAction(self, action):
        # 0 ns left turn
        if action == 0:
            for leftlanes in self.leftlanes:
                self.lanes[0, self.lanes-leftlanes] = 0
                self.lanes[2, self.lanes-leftlanes] = 0
        # 1 ns straight
        elif action == 1:
            for straightlanes in self.lanes-self.leftlanes:
                self.lanes[0, straightlanes] = 0
                self.lanes[2, straightlanes] = 0
        # 2 we left turn
        elif action == 2:
            for leftlanes in self.leftlanes:
                self.lanes[1, self.lanes-leftlanes] = 0
                self.lanes[3, self.lanes-leftlanes] = 0
        # 3 we straight
        else:
            for straightlanes in self.lanes-self.leftlanes:
                self.lanes[1, straightlanes] = 0
                self.lanes[3, straightlanes] = 0
        return self.lanes

    def render(self):
        # implement visulization
        window = tk.Tk()
        pxsize = 50
        pxsizeoffset = 5
        window.geometry(str(pxsize*(self.queuesize*2+self.numlanes)) +
                        'x'+str(pxsize*(self.queuesize*2+self.numlanes)))
        canvas = tk.Canvas(window, width=pxsize*(self.queuesize*2 +
                           self.numlanes), height=pxsize*(self.queuesize*2+self.numlanes))
        canvas.create_rectangle(self.queuesize*pxsize, 0, (self.queuesize+self.numlanes)
                                * pxsize, pxsize*(2*self.queuesize+self.numlanes))
        canvas.create_rectangle(0, self.queuesize*pxsize, pxsize*(
            self.queuesize*2+self.numlanes), pxsize*(self.queuesize+self.numlanes))
        # vertical lines
        for x in range(self.numlanes):
            canvas.create_line((self.queuesize+x+1)*pxsize, 0, (self.queuesize+x+1)
                           * pxsize, pxsize*(2*self.queuesize+self.numlanes))
        # horizontal lines
        for x in range(self.numlanes):
            canvas.create_line(0, (self.queuesize+x+1)*pxsize, pxsize *
                            (2*self.queuesize+self.numlanes), (self.queuesize+x+1)*pxsize)

        # north
        for lane in range(self.numlanes):
            # print(self.lanes[0][lane].spacesFilled())
            for space in range(self.lanes[0, lane]):
                canvas.create_rectangle(pxsize*(self.queuesize+lane)+pxsizeoffset, pxsize *
                                        (self.queuesize-1-space)+pxsizeoffset, pxsize*(self.queuesize+lane+1)-pxsizeoffset, pxsize*(self.queuesize-space)-pxsizeoffset, fill='grey')
        
        # east
            for lane in range(self.numlanes):
                # print(self.lanes[1][lane].spacesFilled())
                for space in range(self.lanes[1, lane]):
                    canvas.create_rectangle(pxsize*(self.queuesize+self.numlanes+space)+pxsizeoffset, pxsize *
                                            (self.queuesize+lane)+pxsizeoffset, pxsize*(self.queuesize+self.numlanes+space+1)-pxsizeoffset, pxsize*(self.queuesize+lane+1)-pxsizeoffset, fill='grey')

        # south
            for lane in range(self.numlanes):
                # print(self.lanes[2][lane].spacesFilled())
                for space in range(self.lanes[2, lane]):
                    canvas.create_rectangle(pxsize*(self.queuesize+self.numlanes-lane-1)+pxsizeoffset, pxsize *
                                            (self.queuesize+self.numlanes+space)+pxsizeoffset, pxsize*(self.queuesize+self.numlanes-lane)-pxsizeoffset, pxsize*(self.queuesize+self.numlanes+space+1)-pxsizeoffset, fill='grey')

        # west
            for lane in range(self.numlanes):
                # print(self.lanes[3][lane].spacesFilled())
                for space in range(self.lanes[3, lane]):
                    canvas.create_rectangle(pxsize*(self.queuesize-space-1)+pxsizeoffset, pxsize *
                                            (self.queuesize+self.numlanes-1-lane)+pxsizeoffset, pxsize*(self.queuesize-space)-pxsizeoffset, pxsize*(self.queuesize+self.numlanes-lane)-pxsizeoffset, fill='grey')
        
        canvas.pack()
        window.mainloop()
        pass

    def reset(self):
        for r in self.lanes:
            for c in self.lanes[r]:
                self.lanes[r, c] = random.randint(0,self.queuesize)
        self.time_length = self.initial_time
        self.state = self.lanes
        return self.state

env = TrafficEnv()
env.render()


# states = env.observation_space.shapes
# actions = env.action_space.n

# def build_model(states, actions):
#     model = Sequential()
#     model.add(Flatten(input_shape=(1,states)))
#     model.add(Dense(24, activation='relu'))
#     model.add(Dense(actions, activation='linear'))
#     return model

