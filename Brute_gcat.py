# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 09:37:38 2020

@author: Shelley
"""

# Class for brute-force calculating the geometric category of a finite space

import FiniteSpaces_Class as FS
import FiniteSpace_Examples as FE
import networkx as nx


def partition(maxs):
    '''

    Parameters
    ----------
    maxs : TYPE
        DESCRIPTION.

    Yields
    ------
    TYPE
        DESCRIPTION.

    '''
    if len(maxs) == 1:
        yield [maxs]
        return

    first = maxs[0]
    for smaller in partition(maxs[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller
        
def is_gcat_cover(space, part):
    for p in part:
        if not(space.getOpens(set(p)).isContractible()):
            return False
    return True

def get_brute_gcat(space):
    maxs = space.getMaxs()
    gc = len(maxs)
    for part in partition(list(maxs)):
        if (len(part)<gc and is_gcat_cover(space,part)):
            gc = len(part)
    return gc
    
            
    
if __name__=='__main__':
    
    K = FE.Build_Klein()
    S = FE.Build_MinCircle()
    
    print("This happened")
    
    for part in partition(list(S.getMaxs())):
        print(is_gcat_cover(S,part))
        print(len(part))