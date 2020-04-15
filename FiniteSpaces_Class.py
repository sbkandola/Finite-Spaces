# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:12:47 2020

@author: Shelley
"""

import networkx as nx
import numpy as np
import operator



class FiniteSpace:


    # Pass in a number k to generate a k-point model of [0,1]
    def __init__(self, inputData): #opens=dict(), k=0):
        '''
        inputData has multiple types:
            if dict, it should be handing me the open sets
            if integer, I'm building a finite model of an interval with k points
            if networkx graph, it's the Hasse diagram
        '''

        if type(inputData) == dict:
            self.opens = inputData
            self.points = set(inputData.keys())
            self.closures = dict()
            self.Hasse = nx.DiGraph()
            self.getHasse()

            # From opens, construct Hasse diagram, keep in self.Hasse

        elif type(inputData) == int:
            k = inputData
            self.opens = {}
            self.closures = {}
            self.Hasse = nx.DiGraph()

            # Note: self.Hasse won't be populated unless necessary

            # Construct the proper Hasse diagram, store as self.Hasse

            if k > 0:
                for i in range(k):
                    if i%2==0:
                        self.opens[str(i)] = set({str(i)})
                    else:
                        self.opens[str(i)] = set({str(max(i-1,0)),str(i),str(min(i+1,k-1))})
                self.points = self.opens.keys()


        elif type(inputData) == nx.DiGraph :

            self.points = set(inputData.nodes)
            self.opens = dict()
            self.closures = dict()
            self.Hasse = inputData

        else:
            print('I did not recognize your input type. Exiting.')


    def __len__(self):
        '''
        Returns
        -------
        The number of points in the space.

        '''
        return len(self.points)

    def getHasse(self):
        '''
        Returns
        -------
        None. Populates self.Hasse with the Hasse diagram of the space.

        '''
        print("Getting Hasse of "+str(self.points))
        self.Hasse.add_nodes_from(self.points)

        for p in self.points:
            p_down = set(self.opens[p])
            for q in self.opens[p]:
                q_up = set(k for (k,v) in self.opens.items() if q in v)
                if len(p_down.intersection(q_up))==2:
                    self.Hasse.add_edge(p,q)

    def getClosures(self):
        '''
        Returns
        -------
        None. Populates the dict self.closures where the keys are points p,
            and the values are all the points q >= p

        '''
        for point in self.points:
            self.closures[point] = set()
            self.closures[point].add(point)
        for point in self.points:
            for other in set(self.points).difference(self.opens[point]):
                if point in self.opens[other]:
                    self.closures[point].add(other)

    def isgeq(self,p1,p2):
        '''
        Parameters
        ----------
        p1 : a point of the space.
        p2 : another point of the space.

        Returns
        -------
        True if p1 >= p2.

        '''
        return self.opens[p1].issuperset(self.opens[p2])

    def isleq(self,p1,p2):
        '''
        

        Parameters
        ----------
        p1 : str
            The name of a point in self.
        p2 : str
            The name of a different point in self.

        Returns
        -------
        bool
            True if p1 <= p2.

        '''
        return self.opens[p1].issubset(self.opens[p2])

    def product(self, space2):
        '''
        

        Parameters
        ----------
        space2 : FiniteSpace
            Any FiniteSpace. There can be an overlap in points.

        Returns
        -------
        FiniteSpace
            The Cartesian product of self and space2.

        '''
        prod = dict()
        for p in self.opens:
            for q in space2.opens:
                prod[p+','+q] = set()
        for p in prod:
            points = p.rsplit(',',1)
            for q in self.opens[points[0]]:
                for r in space2.opens[points[1]]:
                    prod[p].add(q+','+r)
        return FiniteSpace(prod)

    def op(self):
        '''
        

        Returns
        -------
        FiniteSpace
            The dual space of self.

        '''
        if len(self.Hasse)==0:
            self.getHasse()
        return FiniteSpace(self.Hasse.reverse())


    def copy(self):
        '''
        

        Returns
        -------
        FiniteSpace
            A copy of the space that can be modified without changing the original.

        '''
        copyGraph = nx.DiGraph()
        copyGraph.add_nodes_from(self.Hasse.nodes)
        copyGraph.add_edges_from(self.Hasse.edges)
        return FiniteSpace(copyGraph)

    def union(self,space2):
        '''
        

        Parameters
        ----------
        space2 : FiniteSpace

        Returns
        -------
        FiniteSpace
            the union of self with space2.

        '''
        spaceUnion = nx.DiGraph()
        spaceUnion.add_edges_from(self.Hasse.edges)
        spaceUnion.add_edges_from(space2.Hasse.edges)
        spaceUnion = nx.transitive_reduction(spaceUnion)
        return FiniteSpace(spaceUnion)


    def intersection(self, space2):
        '''
        

        Parameters
        ----------
        space2 : FiniteSpace
            another finite space.

        Returns
        -------
        FiniteSpace
            the intersection of self with space2.

        '''
        intNodes = set(self.Hasse.nodes).intersection(space2.Hasse.nodes)
        return FiniteSpace(self.Hasse.subgraph(intNodes))

    def hasEmptyIntersection(self,space2):
        '''
        

        Parameters
        ----------
        space2 : FiniteSpace
            a finite space.

        Returns
        -------
        bool
            Returns true if self and space2 have no points in common.

        '''
        return len(self.intersection(space2))==0

    def join(self, space2):
        '''
        

        Parameters
        ----------
        space2 : FiniteSpace
            A finite space with points different from self

        Returns
        -------
        join : FiniteSpace
            The non-Hausdroff join of self with space2.

        '''
        if set(self.opens).isdisjoint(set(space2.opens)):
            join = self.union(space2)
            for q in space2.opens:
                for p in self.opens:
                    join.opens[q].add(p)
        return join
    
        
    def isOpen(self):
        '''
        Returns
        -------
        True if self is a union of open sets

        '''
        for p in self.opens:
            for q in self.opens[p]:
                if q not in self.opens:
                    return False
        return True

    def isT0(self):
        '''
        Returns
        -------
        True if self is T_0 (i.e., given any two points, 
                             there exists an open set that contains one point
                             and not the other)
        '''
        for p in self.opens:
            for q in self.opens:
                if (self.opens[p]==self.opens[q])&(p!=q):
                    return False
        return True

    def getDownset(self,point):
        '''
        Parameters
        ----------
        point : a point from self.

        Returns
        -------
        A FiniteSpace that is the minimal open neighborhood containing point
        '''
        downnodes = nx.descendants(self.Hasse,point)
        downnodes.add(point)
        return FiniteSpace(self.Hasse.subgraph(downnodes))

    def getPuncturedDownset(self,point):
        '''
        Parameters
        ----------
        point : a point of self.

        Returns
        -------
        A FiniteSpace that is the Downset of point, minus point

        '''
        downnodes = nx.descendants(self.Hasse,point)
        return FiniteSpace(self.Hasse.subgraph(downnodes))


    def getUpset(self,point):
        '''
        Parameters
        ----------
        point : a point from self.

        Returns
        -------
        A FiniteSpace that is the closure of point
        '''
        upnodes = nx.ancestors(self.Hasse,point)
        upnodes.add(point)
        return FiniteSpace(self.Hasse.subgraph(upnodes))

    def getPuncturedUpset(self,point):
        '''
        Parameters
        ----------
        point : a point of self.

        Returns
        -------
        A FiniteSpace that is the Upset of point, minus point

        '''
        upnodes = nx.ancestors(self.Hasse,point)
        return FiniteSpace(self.Hasse.subgraph(upnodes))

    def hasUniqueMax(self):
        '''
        Returns
        -------
        True if self has a unique maximal element.

        '''
        if len(self.Hasse)==0:
            self.getHasse()
        in0 = [n for n in self.Hasse.nodes if self.Hasse.in_degree(n)==0]
        return len(in0)==1

    def getUniqueMax(self):
        '''
        If a space has a unique maximal element, it returns that element
        
        Returns
        -------
        A point from self.

        '''
        if len(self.Hasse)==0:
            self.getHasse()
        in0 = [n for n in self.Hasse.nodes if self.Hasse.in_degree(n)==0]
        if len(in0)==1:
            return in0[0]

    def hasUniqueMin(self):
        '''
        Returns
        -------
        True if self has a unique minimal element.

        '''
        if len(self.Hasse)==0:
            self.getHasse()
        out0 = [n for n in self.Hasse.nodes if self.Hasse.out_degree(n)==0]
        return len(out0)==1

    def getUniqueMin(self):
        '''
        If self has a unique minimal element, it returns that element

        Returns
        -------
        A point of self.

        '''
        if len(self.Hasse)==0:
            self.getHasse()
        out0 = [n for n in self.Hasse.nodes if self.Hasse.out_degree(n)==0]
        if len(out0)==1:
            return out0[0]

    def isBeat(self,point):
        '''
        Determines if either the punctured upset of point has a unique min,
            or the punctured downset of point has a unique max

        Parameters
        ----------
        point : a point of self.

        Returns
        -------
        True if point is beat.

        '''
        test1 = self.Hasse.in_degree(point)==1
        test2 = self.Hasse.out_degree(point)==1
        return (test1|test2)

    def hasBeat(self):
        '''
        Returns
        -------
        bool
            True if any points of self are beat.

        '''
        for p in self.points:
            if self.isBeat(p):
                return True

    def getBeat(self):
        '''
        Returns an arbitrary beat point of self                
        Returns
        -------
        p : the name of a point in self.

        '''
        for p in self.points:
            if self.isBeat(p):
                return p

    def hasGetBeat(self):
        '''
        Determines if self has a beat point, and if so, what that beat point is
        Note: the beat point may not be unique!
            
        Returns
        -------
        bool
            True if self has a beat point, False if it doesn't.
        TYPE
            The name of the beat point, or an empty string.

        '''
        for p in self.points:
            if self.isBeat(p):
                return (True,p)
        return (False,'')


    def delBeat(self,point):
        '''
        Returns a strong deformation retract of self onto self-{point}
        This should only be run if "point" is beat

        Parameters
        ----------
        point : the name of a point in self, as a string.

        Returns
        -------
        A FiniteSpace that is self-{point}.

        '''
        newGraph = nx.DiGraph()
        newGraph.add_nodes_from(self.Hasse.nodes)
        newGraph.add_edges_from(self.Hasse.edges)
        newGraph.remove_node(point)

        for p in nx.ancestors(self.Hasse,point):
            for q in nx.descendants(self.Hasse,point):
                newGraph.add_edge(p,q)

        newGraph = nx.transitive_reduction(newGraph)
        return FiniteSpace(newGraph)


    def getCore(self):
        '''
        Returns
        -------
        core : FiniteSpace
            A space homotopy equivalent to self that has no beat points.

        '''
        core = self
        (y,p) = core.hasGetBeat()
        while(y):
            core = core.delBeat(p)
            (y,p) = core.hasGetBeat()
        return core

    def isContractible(self):
        '''
        Determines if self is contractible.
            If self only has 2 maximal elements, it checks to see if the intersection of the downsets of those two max elts is contractible
            Otherwise, it gets the core of the entire space

        Returns
        -------
        bool
            True if the core of self is 1 point.

        '''
        maxs = list(self.getMaxs())
        if len(maxs)==2:
            return self.twoDownContractible(maxs[0],maxs[1])
        else:
            return len(self.getCore().points)==1

    def isContractibleComponents(self):
        '''
        Determines if self is a union of contractible sets

        Returns
        -------
        bool
            True if self is a union of contractible open sets.

        '''
        comps = nx.weakly_connected_components(self.Hasse)
        for comp in comps:
            if not FiniteSpace(self.Hasse.subgraph(comp)).isContractible():
                return False
        return True

    def twoDownContractible(self, max1, max2):
        '''
        

        Parameters
        ----------
        max1 : str
            The name of a point of self.
        max2 : str
            The name of a point of self.

        Returns
        -------
        bool
            DESCRIPTION.

        '''
        space1 = self.getDownset(max1)
        space2 = self.getDownset(max2)
        S1intS2 = space1.intersection(space2)
        if len(S1intS2)==0:
            return False
        else:
            return space1.intersection(space2).isContractible()

    # Returns a SET of the maximal elements of a SPACE
    def getMaxs(self):
        if not self.Hasse:
            self.getHasse()
        maxs = set(n for n in self.Hasse.nodes if self.Hasse.in_degree(n)==0)
        return maxs

    # Greedy algorithm builds the largest contratctible subset
    # # of a space that it can by randomly adding other downsets
    def buildMaxContractible(self):
        maxs = self.getMaxs()
        candidate = self.getDownset(maxs.pop())
        while len(maxs)>0:
            nextSet = self.getDownset(maxs.pop())
            nextNextSet = candidate.union(nextSet)
            if nextNextSet.isContractible():
                candidate = candidate.union(nextNextSet)
        return candidate

    def buildMaxCat(self):
        '''
        Approximates the geometric category of a finite space

        Returns
        -------
        maxCover : list
            Returns a list of finite spaces whose union covers self.

        '''
        maxCover = []
        maxs = self.getMaxs()
        m = maxs.pop()
        maxCover.append(self.getDownset(m))
        unHasse = self.Hasse.to_undirected()
        unHasse_dict = nx.shortest_path_length(unHasse, m)
        sorted_dict = sorted(unHasse_dict.items(), key=operator.itemgetter(1))
        sorted_maxs = [key[0] for key in sorted_dict if key[0] in maxs]
        for m in sorted_maxs:
            #print('working on m =',m)
            #print('Current cover list is ', [ cover.getMaxs() for cover in maxCover])
            found = False
            nextMax = self.getDownset(m)
            for c in range(len(maxCover)):
               testUnion = maxCover[c].union(nextMax)
               if (testUnion.isContractibleComponents()) or (nextMax.hasEmptyIntersection(maxCover[c])):
                   maxCover[c] = testUnion
                   found = True
                   break
            if found==False:
                maxCover.append(nextMax)
            #print('Current cover list is ', [ cover.getMaxs() for cover in maxCover])
        return maxCover



    # returns the union of downsets of a list of elements
    def getOpens(self,elts):
        newElts = set(elts)
        #newElts = set()
        for e in elts:
            #newElts.add(e)
            #newElts.add(set({nx.descendants(self.Hasse,e)}))
            newElts = newElts.union(set(nx.descendants(self.Hasse,e)))
        return FiniteSpace(self.Hasse.subgraph(newElts))


    # Estimates the gcat of a space
    def gcat(self):
        maxs = self.getMaxs()
        gc = 0
        while len(maxs)>0:
            cover = self.getOpens(maxs).buildMaxContractible()
            usedMaxs = cover.getMaxs()
            maxs.difference_update(usedMaxs)
            gc = gc + 1
        return gc

    # gets the height of a point in a Hasse diagram
    def getHeight(self,point):
        if len(self.Hasse)==0:
            self.getHasse()
        return len(nx.dag_longest_path(nx.dfs_tree(self.Hasse,point)))-1

    # gets the level of every point in a space
    def getLevels(self):
        levelDict = dict()
        for p in self.points:
            levelDict[p] = self.getHeight(p)
        return levelDict

    # create a level dictionary for graphing later
    def setLevels(self):
        if len(self.Hasse)==0:
            self.getHasse()
        levelDict = self.getLevels()
        for p in self.Hasse.nodes:
            self.Hasse.nodes[p]['level'] = levelDict[p]

    def findDrawingPositions(self):
        pos_y_Dict = self.getLevels()
        levelDict={i:[]for i in set(pos_y_Dict.values())}
        for v in pos_y_Dict.keys():
            levelDict[pos_y_Dict[v]].append(v)

        posDict = {}
        for level in levelDict.keys():
            verts = levelDict[level]
            numInLevel = len(verts)
            if numInLevel==1:
                v = verts[0]
                posDict[v]=(0.5, pos_y_Dict[v])
            else:
                for i,v in enumerate(verts):
                    posDict[v] = np.array([i/(numInLevel-1), pos_y_Dict[v]])

        return posDict

    def drawHasse(self):
        if len(self.Hasse)==0:
            self.getHasse()
        pos = self.findDrawingPositions()
        nx.draw(self.Hasse,pos, with_labels = True, node_color = 'purple', font_color = 'grey', font_weight = 'bold')
