# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 09:37:38 2020

@author: Shelley
"""

# Class for brute-force calculating the geometric category of a finite space

import FiniteSpace_Examples as FE
# import more_itertools as mit
from itertools import combinations


def partition(items, k):
    '''

    Parameters
    ----------
    maxs : a list of elements.

    Yields
    ------
    An iterator of all possible partitionings of size $k$ of those elements.

    '''
    if len(items) == 1:
        yield [items]
        return

    # From https://stackoverflow.com/questions/23596702/iterating-over-partitions-in-python
    def split(indices):
        i=0
        for j in indices:
            yield items[i:j]
            i = j
        yield items[i:]

    for indices in combinations(range(1, len(items)), k-1):
        yield list(split(indices))

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




def get_brute_gcat(space, verbose = False):
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

    for k in range(gc, 0, -1): # Search going down from a cover of size gc
        if verbose:
            print("Trying covers of size",k)

        # Start checking for a partition of size $k$ that is a valid cover
        for part in partition(list(maxs), k):
            if is_gcat_cover(space,part):
                # If you're in here, you have a valid cover.
                gc = len(part)
                if verbose:
                    print('\tFound cover of size', gc)
                k += 1
                break
            # If you didn't break, you didn't find a cover
            if verbose:
                print('No cover found of size', k,"so min size cover is",str(gc)+"... exiting.")
            return gc



if __name__=='__main__':

    K = FE.Build_Klein()
    S = FE.Build_MinCircle()


    for part in partition(list(S.getMaxs())):
        print(is_gcat_cover(S,part))
        print(len(part))
