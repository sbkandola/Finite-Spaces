# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 09:37:38 2020

@author: Shelley
"""

# Class for brute-force calculating the geometric category of a finite space

import FiniteSpace_Examples as FE


def partition(maxs):
    '''

    Parameters
    ----------
    maxs : a list of elements.

    Yields
    ------
    A generator of all possible partitionings of those elements.

    '''
    if len(maxs) == 1:
        yield [maxs]
        return

    first = maxs[0]
    for smaller in partition(maxs[1:]):
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        yield [ [ first ] ] + smaller
        
def is_gcat_cover(space, part):
    '''
    

    Parameters
    ----------
    space : a FiniteSpace
    part : a partitioning of the maximal elements of space.

    Returns
    -------
    bool
        True if every open set of SPACE determined by PART is contractible,
    and False if at least one of the open sets is not contractible.

    '''
    for p in part:
        if not(space.getOpens(set(p)).isContractible()):
            return False
    return True

def get_brute_gcat(space):
    '''
    

    Parameters
    ----------
    space : a finite topological space from FiniteSpaces_Class.

    Returns
    -------
    gc : the minimal number of contractible open sets required to cover SPACE

    '''
    maxs = space.getMaxs()
    gc = len(maxs)
    for part in partition(list(maxs)):
        if (len(part)<gc and is_gcat_cover(space,part)):
            gc = len(part)
    return gc
    
            
    
if __name__=='__main__':
    
    K = FE.Build_Klein()
    S = FE.Build_MinCircle()
    
    
    for part in partition(list(S.getMaxs())):
        print(is_gcat_cover(S,part))
        print(len(part))