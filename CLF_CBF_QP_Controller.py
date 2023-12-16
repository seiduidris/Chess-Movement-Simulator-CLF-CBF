
'''

Author: Idris Seidu

'''



from gurobipy import *

import math

import numpy as np

import matplotlib.pyplot as plt
from gurobipy import Model, GRB
import numpy as np



class QPcontroller:

    def __init__(self, config={}):

        self.k_cbf = 1 #CBF coefficient

        self.epsilon = 0.4 #Finite time CLF coefficient

        self.m = Model("CBF_CLF_QP")

        self.num_of_states = 2

        self.num_of_control_inputs = 2

        self.u1_upper_lim = 10000 # From Create Autonomy

        self.u1_lower_lim = -10000

        self.u2_upper_lim = 10000

        self.u2_lower_lim = -10000


    


        self.dt = 0.4

        self.goal = None



        # Control Variables

        self.u1 = self.m.addVar(lb=self.u1_lower_lim, ub=self.u1_upper_lim,vtype=GRB.CONTINUOUS, name="x1_input_acceleration")

        self.u2 = self.m.addVar(lb=self.u2_lower_lim, ub=self.u2_upper_lim,vtype=GRB.CONTINUOUS, name="x2_input_acceleration")





    def set_goal(self, goal):

        self.goal = goal



    def get_next_wp(self, action=None, curr_pose=None, curr_vel=None, obs_info={}):

        _, target_vel, target_pose = self.generate_control(curr_pose, obs_info)

        return None, target_vel, target_pose



    def generate_control(self,x_current, obs_info={}):

        #self.m.reset()
        self.m.remove(self.m.getConstrs())
        V = (x_current[0]-self.goal[0])**2 + (x_current[1]-self.goal[1])**2



        partial_V_x1 = (x_current[0]-self.goal[0])

        partial_V_x2 = (x_current[1]-self.goal[1])


        self.m.addConstr(2*partial_V_x1*self.u1 + 2*partial_V_x2*self.u2 + self.epsilon*V <= 0, "Relaxed_CLF_constraint")

         # Initialize Cost Function

        self.cost_func = self.u1*self.u1+self.u2*self.u2 

        self.m.setObjective(self.cost_func,GRB.MINIMIZE)


        #Stop optimizer from publsihing results to console - remove if desired

        self.m.Params.LogToConsole = 0



        #Solve the optimization problem

        self.m.optimize()

        self.solution = self.m.getVars()

         # get final decision variables

        self.control_u1 = self.solution[0].x

        self.control_u2 = self.solution[1].x

        #self.control_u3 = self.solution[2].x

        # Loop through sphereical obstacles and set constraints
        self.m.remove(self.m.getConstrs())

        num_of_obstacles = len(obs_info) #For later use when more obstacles are involved


        x_current_radius = 0.5
        # Loop through sphereical obstacles and set constraints

        for i in range(0,num_of_obstacles):

            pos = obs_info[i]['position']

            rad = obs_info[i]['radius']
            

            h = (x_current[0]-pos[0])**2 + (x_current[1]-pos[1])**2  - (rad + x_current_radius+ 0.1)**2

            self.m.addConstr(2*(x_current[0]-pos[0])*self.u1 + 2*(x_current[1]-pos[1])*self.u2  + self.k_cbf*h >= 0)


        self.cost_func_new = (self.u1-self.control_u1)*(self.u1- self.control_u1)+(self.u2-self.control_u2)*(self.u2-self.control_u2) 

        self.m.setObjective(self.cost_func_new,GRB.MINIMIZE)

        
        self.m.optimize()

        self.solution_new = self.m.getVars()



        # get final decision variables

        self.control_u1_new = self.solution_new[0].x

        self.control_u2_new = self.solution_new[1].x

        self.m.write("qp_model.lp")



        target_vel = np.array([self.control_u1_new, self.control_u2_new])



        target_pose = x_current + target_vel * self.dt





        # return None, None, target_pose

        return None, target_vel, target_pose


