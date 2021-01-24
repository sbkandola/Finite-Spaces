# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:33:45 2020

@author: kandola2
"""

# Testing Finite Spaces

import FiniteSpaces_Class as FS
import networkx as nx



def Build_Test_SC():
    '''
    

    Returns
    -------
    SC : FiniteSpace
        A space that has different LS category and geometric category.

    '''
    SC = FS.FiniteSpace(dict({
        'abc': set({'abc','ab','ac','bc'}),
        'ab': set({'ab','a','b'}),
        'ac': set({'ac','a','c'}),
        'bc': set({'bc','b','c'}),
        'ad': set({'ad','a','d'}),
        'a': set({'a'}),
        'b': set({'b'}),
        'c': set({'c'}),
        'd': set({'d'})}))
    return SC

def Build_Klein():
    '''
    

    Returns
    -------
    Klein : returns the minimal finite model of the Klein bottle 
        as an object of FiniteSpaces_Class.

    '''
    Klein = FS.FiniteSpace(dict({
            'a1': set({'a1', 'b1', 'b2','b3','b4','c1','c2','c3','c4'}),
            'a2': set({'a2', 'b1', 'b2','b5','b6','c1','c2','c3','c4'}),
            'a3': set({'a3', 'b3', 'b5','b7','b8','c1','c2','c3','c4'}),
            'a4': set({'a4', 'b4', 'b6','b7','b8','c1','c2','c3','c4'}),
            'b1': set({'b1','c1','c3'}),
            'b2': set({'b2','c2','c4'}),
            'b3': set({'b3','c3','c4'}),
            'b4': set({'b4','c1','c2'}),
            'b5': set({'b5','c1','c2'}),
            'b6': set({'b6','c3','c4'}),
            'b7': set({'b7','c1','c3'}),
            'b8': set({'b8','c2','c4'}),
            'c1': set({'c1'}),
            'c2': set({'c2'}),
            'c3': set({'c3'}),
            'c4': set({'c4'})}))
    return Klein

def Build_NotCont():
    '''
    

    Returns
    -------
    NotCont : FiniteSpace
        A finite space that isn't contractible.

    '''
    NotCont = FS.FiniteSpace(dict({
        'x1': set({'x1','y1','y2','z1','z2'}),
        'x2': set({'x2','y1','y2','y3','z1','z2'}),
        'x3': set({'x3','y3','y4','y5','z3','z4'}),
        'x4': set({'x4','y4','y5','z3','z4'}),
        'y1': set({'y1','z1','z2'}),
        'y2': set({'y2','z1','z2'}),
        'y3': set({'y3'}),
        'y4': set({'y4','z3','z4'}),
        'y5': set({'y5','z3','z4'}),
        'z1': set({'z1'}),
        'z2': set({'z2'}),
        'z3': set({'z3'}),
        'z4': set({'z4'})
        }))
    return NotCont
    

def Build_MinCircle():
    '''
    

    Returns
    -------
    MinCircle : The minimal finite model of S^1 
        as an object of FiniteSpaces_Class.

    '''
    MinCircle = FS.FiniteSpace(dict({'a': set({'a','c','d'}),
           'b': set({'b','c','d'}),
           'c': set({'c'}),
           'd': set({'d'})}))
    return MinCircle

def Build_S1_3():
    '''
    

    Returns
    -------
    SixCircle : A finite model of S1 with 3 maximal elements.

    '''

    SixCircle = FS.FiniteSpace(dict({
            'y0': set({'y0','x0','x1'}),
            'y1': set({'y1','x1','x2'}),
            'y2': set({'y2','x2','x0'}),
            'x0': set({'x0'}),
            'x1': set({'x1'}),
            'x2': set({'x2'})
        }))
    return SixCircle

def Build_S1_4():
    '''
    

    Returns
    -------
    SixCircle : A finite model of S1 with 4 maximal elements.

    '''

    SixCircle = FS.FiniteSpace(dict({
            'y0': set({'y0','x0','x1'}),
            'y1': set({'y1','x1','x2'}),
            'y2': set({'y2','x2','x3'}),
            'y3': set({'y3','x3','x0'}),
            'x0': set({'x0'}),
            'x1': set({'x1'}),
            'x2': set({'x2'}),
            'x3': set({'x3'})
        }))
    return SixCircle

def Build_S1_5():
    '''
    

    Returns
    -------
    TenCircle : A finite model of a circle with 5 maximal elements.

    '''
    TenCircle = FS.FiniteSpace(dict({
            'y0': set({'y0','x0','x1'}),
            'y1': set({'y1','x1','x2'}),
            'y2': set({'y2','x2','x3'}),
            'y3': set({'y3','x3','x4'}),
            'y4': set({'y4','x4','x0'}),
            'x0': set({'x0'}),
            'x1': set({'x1'}),
            'x2': set({'x2'}),
            'x3': set({'x3'}),
            'x4': set({'x4'})
        }))
    return TenCircle

def Build_MinTorus():
    '''
    

    Returns
    -------
    MinTorus : the minimal finite model of a Torus
        as an object from FiniteSpaces_Class.

    '''
    MinCircle = Build_MinCircle()
    MinTorus = MinCircle.product(MinCircle)
    return MinTorus

def Build_T2_9():
    '''
    

    Returns
    -------
    SixTorus : A finite model of the torus with 9 maximal elements.

    '''
    SixCircle = Build_S1_3()
    SixTorus = SixCircle.product(SixCircle)
    return SixTorus

def Build_T2_25():
    '''
    

    Returns
    -------
    TenTorus : A model of T2 with 25 maximal elements.

    '''
    TenCircle = Build_S1_5()
    TenTorus = TenCircle.product(TenCircle)
    return TenTorus

def Build_KleinSquared():
    '''
    

    Returns
    -------
    KleinSquared : The square of the Klein bottle
        as an object from FiniteSpaces_Class.

    '''
    Klein = Build_Klein()
    KleinSquared = Klein.product(Klein)
    return KleinSquared

def Build_Disjoint():
    '''
    

    Returns
    -------
    The disjoint union of two minimal models of [0,1]
        as an object from FiniteSpaces_Class.

    '''
    disjointHasse = nx.DiGraph()
    disjointHasse.add_nodes_from('abcd')
    disjointHasse.add_edge('a','b')
    disjointHasse.add_edge('c','d')
    return FS.FiniteSpace(disjointHasse)

def Build_Int3():
    '''
    

    Returns
    -------
    Int3 : A 3-point model of [0,1]
        as an object of FiniteSpaces_Class.

    '''
    Int3 = FS.FiniteSpace(dict({'b': set({'a','b','c'}),
           'a': set({'a'}),
           'c': set({'c'})}))
    return Int3

if __name__=='__main__':
    Klein = Build_Klein()
    print(Klein.opens)
    Klein.drawHasse()

