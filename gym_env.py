from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import os 
import sys 
import optparse
import random
import time
from sumolib import checkBinary
import traci
from PTS_Int import docparse


def run(x):
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, '-c', 'highway.sumocfg',"--tripinfo-output", "tripinfo.xml", "-S", "--quit-on-end"]);
    step = 0
    x1 = x[0]
    y1 = x[1]
    dectstring = "det_" + str(x1) + "_" + str(y1)
    lanenum = "E" + str(x1)
    lanes=[0,1,2]
    lanes.remove(x1)
    laneoption1 = lanes[0]
    laneoption2 = lanes[1]
    while traci.simulation.getMinExpectedNumber() > 0:
        time.sleep(.005) ######### <------ Here you can adjust the Playback speed (helpful to lower for more iterations)
        traci.simulationStep()
        #print(step)
        det_vehs3 = traci.inductionloop.getLastStepVehicleIDs("det_4") ##ROADBLOCK
        det_vehs2 = traci.inductionloop.getLastStepVehicleIDs(dectstring) ###Decide to Move Lanes here 
        for V in det_vehs2: ### Run a Loop to change lanes 
            can_Merge = traci.vehicle.couldChangeLane(V,10)
            if can_Merge == True :
                try:
                    traci.vehicle.changeLane(V,laneoption1,25)
                    #print('C',V,laneoption1)
                except traci.exceptions.TraCIException:
                    traci.vehicle.changeLane(V,laneoption2,25)
                    #print('C',V,laneoption2)
            elif can_Merge == False:
                traci.vehicle.setStop(V,'E0',duration=1,startPos=280,pos=289,until=1)
                #print('Slowed')
                try:
                    traci.vehicle.changeLane(V,laneoption1,25)
                    #print('C',V,laneoption1)
                except traci.exceptions.TraCIException:
                    traci.vehicle.changeLane(V,laneoption2,25)
                    #print('C',V,laneoption2)
            #print(V,"Tried Merging ",traci.vehicle.couldChangeLane(V,10)) ###Results True/False if the Car can Change lanes
            #print("Change_Lane",traci.vehicle.changeLane(V,0,25)) ### Results if car can change lane 
        for vehs in det_vehs3:
            #print(vehs)
            try:
                traci.vehicle.setStop(vehs,'E0',duration=1,startPos=280,pos=289,until=1)
                traci.vehicle.changeLane(vehs, 2, 25)
            except traci.exceptions.TraCIException:
                print("VERY BAD")
        step += 1
        #print("Traci Expected Number", traci.simulation.getMinExpectedNumber())
        #print("Step",step)
    traci.close()
    sys.stdout.flush()





class TrafficEnv1(Env):
    def __init__(self):
        self.action_space = Discrete(12)
        self.observation_space = Box(low=np.array([0]), high=np.array([5]))
        self.state = 0
        self.length = 5 
    def step(self, action):
        run((1,action))
        x = docparse.getresults()
        y = random.uniform(0,.2)
        x = x % 1
        x = x - y
        self.state = x
        self.length -= 1
        
        if self.state > .5:
            reward = x
        else:
            reward = x
            
        if self.length <= 0:
            done = True
        else:
            done = False
        
        info = {}
        
        return self.state, reward, done, info

    def render(self):
        sumoBinary = checkBinary('sumo-gui')
        pass
    def reset(self):
        self.state = 0
        self.length = 5
        return self.state