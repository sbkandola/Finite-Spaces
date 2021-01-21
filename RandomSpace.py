# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:35:15 2021

@author: shell
"""


import networkx as nx
import numpy as np
import operator
import random
import FiniteSpaces_Class as FS

   
v  = 10
p=.2


def randomSpace(points, probability):
    v = points
    p = probability
    
    # add the nodes
    space = nx.DiGraph()
    space.add_nodes_from(range(v))
    
    # establish the height dictionary
    # all lone points are of height 0
    height_dict = {}
    for i in range(v):
        height_dict[i] = 0
        
    for point1 in space.nodes:
       for point2 in space.nodes:
           if (height_dict[point2]==0 or height_dict[point1] > height_dict[point2]) and (point1 != point2):
               if random.random()<p:
                   space.add_edge(point1, point2)
                   # Sometimes, the height might not increase! Need to fix the line below.
                   height_dict[point1] = max(height_dict[point1], height_dict[point2]+1)
                   
    space = nx.transitive_reduction(space)
    Space = FS.FiniteSpace(space)
    return Space
   