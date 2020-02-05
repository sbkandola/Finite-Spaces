# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 20:14:04 2020

@author: Shelley
"""
import FiniteSpaces_Class

class FiniteFunction:
    
    def __init__(self, space1, space2, function):
        self.space1 = space1
        self.space2 = space2
        self.function = function
        
    def isContinuous(self):
        for i in self.function.keys():
            for j in self.function.keys():
                if self.space1.isleq(i,j):
                    #print('Comparing '+str(i)+' and '+str(j))
                    if not self.space2.isleq(self.function[i],self.function[j]):
                        return False
        return True
    
    # Test maps
    # I3 =  {'0': {'0'}, '1': {'0', '1', '2'}, '2': {'2'}}
    # id3 = {'0': '0', '1': '1', '2': '2'}
    # Id3 = FF.FiniteFunction(I3,I3,id3)
    # Id3.isContinuous() returns True!!