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
    Code from:
    https://codereview.stackexchange.com/questions/1526/finding-all-k-subset-partitions

    Uses Algorithm U, described by Knuth in the Art of Computer Programming, Volume 4,
    Fascicle 3B.

    Parameters
    ----------
    items : a list of elements
    k : an integer, the number of sets in the partition

    Yields
    ------
    An iterator of all possible partitionings of size $k$ of the elements.

    '''
    m = k

    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(items[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(items)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)






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




def get_brute_gcat(space, verbose = False, upper = None):
    '''

    Parameters
    ----------
    space : a finite topological space from FiniteSpaces_Class.

    Returns
    -------
    gc : the minimal number of contractible open sets required to cover SPACE

    '''
    maxs = space.getMaxs()
    
    
    keepLooking = True
    if not upper:
        gc = len(maxs)
    else:
        gc = upper


    while keepLooking: 
        # print('k = ',k, 'and gc=',gc)
        # Start checking for a partition of size $k$ that is a valid cover
        
        
        
        for k in range(gc,1,-1):
            if k < gc - 1:
                if verbose:
                    print('k has decreased twice to',k,' without improving gc, which is',gc,'... exiting')
                keepLooking = False
                break
            if verbose:
                print('Checking partitions of size',k, 'while gc =',gc)
            for part in partition(list(maxs), k):
                if is_gcat_cover(space, part):
                    # If you're in here, you have a valid cover.
                    print(part)
                    gc = k
                    if verbose:
                        print('\tFound cover of size', k)
                    break
        
        
            if k==2:
                if verbose:
                    print('Manually going from 2 to 1')
                k-=1
                # I realize this is goofy, but it doesn't add too much extra time
        
            
        if k == 1:
            # If you got down to 2, test 1
            print('k = 1')
            part = [maxs]
            if is_gcat_cover(space, part):
                print(part)
                gc = len(part)
                print('\tFound cover of size', gc)
                return gc
            else:
                print('\tNo cover found of size', len(part),'... exiting.')
                return gc
        
    return gc


if __name__=='__main__':

    K = FE.Build_Klein()
    S = FE.Build_MinCircle()


    for part in partition(list(S.getMaxs())):
        print(is_gcat_cover(S,part))
        print(len(part))
