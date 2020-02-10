# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:12:47 2020

@author: Shelley
"""

import networkx as nx
import numpy as np



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
            print('You gave me a dictionary of the open sets...')
            self.opens = inputData
            self.points = set(inputData.keys())
            self.closures = dict()
            self.Hasse = nx.DiGraph()
            self.getHasse()
            
            # From opens, construct Hasse diagram, keep in self.Hasse

        elif type(inputData) == int:
            print('You want a finite model of the interval... ')
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
            print('You gave me the Hasse diagram....')
            
            self.points = set(inputData.nodes)
            self.opens = dict()
            self.closures = dict()
            self.Hasse = inputData
            
            for p in self.points:
                self.opens[p] = set()
                for q in nx.descendants(inputData,p):
                    self.opens[p].add(q)
                self.opens[p].add(p)

            # Given a nx.Digraph type, populate self.opens, self.points, self.closures
            # Store graph as self.Hasse
            # Add the level of the node as an attribute (later helpful for drawing)

        else:
            print('I did not recognize your input type. Exiting.')


    # Returns the # of points in a space
    def __len__(self):
         return len(self.points)

    # Populates self.Hasse if the method uses it...
     # probably a better way to do this :(
    def getHasse(self):
        self.Hasse.add_nodes_from(self.points)

        for p in self.points:
            p_down = set(self.opens[p])
            for q in self.opens[p]:
                q_up = set(k for (k,v) in self.opens.items() if q in v)
                if len(p_down.intersection(q_up))==2:
                    self.Hasse.add_edge(p,q)
    
    # Populates "self.closures"
    def getClosures(self):
        for point in self.points:
            self.closures[point] = set()
            self.closures[point].add(point)
        for point in self.points:
            for other in set(self.points).difference(self.opens[point]):
                # if point <= other:
                if point in self.opens[other]:
                    # add other to the closure of point
                    self.closures[point].add(other)

    # returns if p1 >= p2
    def isgeq(self,p1,p2):
        return self.opens[p1].issuperset(self.opens[p2])

    # returns if p1 <= p2
    def isleq(self,p1,p2):
        return self.opens[p1].issubset(self.opens[p2])

    # Returns the product of self with another space
    def product(self, space2):
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
    
    # Returns the dual of a space
    def op(self):
        if len(self.Hasse)==0:
            self.getHasse()
        return FiniteSpace(self.Hasse.reverse())

    # copies a finite space IS THIS A WASTE OF TIME?
    def copy(self):
        newSet = dict()
        for p in self.opens:
            newSet[p] = set(self.opens[p])
        return FiniteSpace(newSet)

    # returns the union of self with another space
    def Union(self,space2):
        union = dict(self.opens)
        for p in set(space2.opens).difference(set(self.opens)):
            union[p] = set(space2.opens[p])
        return FiniteSpace(union)
    
    # I think this works now!
    def union(self,space2):
        spaceUnion = nx.DiGraph()
        spaceUnion.add_edges_from(self.Hasse.edges)
        spaceUnion.add_edges_from(space2.Hasse.edges)
        spaceUnion = nx.transitive_reduction(spaceUnion)
        return FiniteSpace(spaceUnion)

    def intersection(self, space2):
        intersection = dict()
        for p in set(self.points).intersection(set(space2.points)):
            intersection[p] = set(self.opens[p])
        return FiniteSpace(intersection)

    # Returns the non-Hausdorff join of a space
    def join(self, space2):
        if set(self.opens).isdisjoint(set(space2.opens)):
            join = self.union(space2)
            for q in space2.opens:
                for p in self.opens:
                    join.opens[q].add(p)
        return join

    def isOpen(self):
        for p in self.opens:
            for q in self.opens[p]:
                if q not in self.opens:
                    return False
        return True

    # Determines if a set is T0
    def isT0(self):
        for p in self.opens:
            for q in self.opens:
                if (self.opens[p]==self.opens[q])&(p!=q):
                    return False
        return True

    # I don't think we need this method anymore vvv
    def getdownset(self,point):
        downset = dict({k:v for (k,v) in self.opens.items() if k in self.opens[point]})
        return FiniteSpace(downset)
    
    def getDownset(self,point):
        downnodes = nx.descendants(self.Hasse,point)
        downnodes.add(point)
        return FiniteSpace(self.Hasse.subgraph(downnodes))

    def getPuncturedDownset(self,point):
        downnodes = nx.descendants(self.Hasse,point)
        return FiniteSpace(self.Hasse.subgraph(downnodes))


    def getUpset(self,point):
        upnodes = nx.ancestors(self.Hasse,point)
        upnodes.add(point)
        return FiniteSpace(self.Hasse.subgraph(upnodes))

    def getPuncturedUpset(self,point):
        upnodes = nx.ancestors(self.Hasse,point)
        return FiniteSpace(self.Hasse.subgraph(upnodes))

    # Determines if a space has a unique maximal element
    def hasUniqueMax(self):
        if len(self.Hasse)==0:
            self.getHasse()
        in0 = [n for n in self.Hasse.nodes if self.Hasse.in_degree(n)==0]
        return len(in0)==1

    # Returns the unique maximal element of a set
    def getUniqueMax(self):
        if len(self.Hasse)==0:
            self.getHasse()
        in0 = [n for n in self.Hasse.nodes if self.Hasse.in_degree(n)==0]
        if len(in0)==1:
            return in0[0]

    # Determines if a space has a unique minimal element
    def hasUniqueMin(self):
        if len(self.Hasse)==0:
            self.getHasse()
        out0 = [n for n in self.Hasse.nodes if self.Hasse.out_degree(n)==0]
        return len(out0)==1

    # Returns the unique minimal element of a set
    def getUniqueMin(self):
        if len(self.Hasse)==0:
            self.getHasse()
        out0 = [n for n in self.Hasse.nodes if self.Hasse.out_degree(n)==0]
        if len(out0)==1:
            return out0[0]

    # Determines if a point in a space is beat
    def isBeat(self,point):
        test1 = self.Hasse.in_degree(point)==1
        test2 = self.Hasse.out_degree(point)==1
        #test1 = self.getPuncturedDownset(point).hasUniqueMax()
        #test2 = self.getPuncturedUpset(point).hasUniqueMin()
        return (test1|test2)

    # Determines if a space has a beat point
    def hasBeat(self):
        for p in self.points:
            if self.isBeat(p):
                return True

    # How can I control the randomness of this method?
    def getBeat(self):
        for p in self.points:
            if self.isBeat(p):
                return p

    # Returns an ordered pair indicating if the space has a beat point,
    # and if so, what that beat point is
    def hasGetBeat(self):
        for p in self.points:
            if self.isBeat(p):
                return (True,p)
        return (False,'')

    # Returns a homotopy equivalent
    def delBeat(self,point):
        #newNodes = set(self.Hasse.nodes)
        #newNodes.remove(point)
       newOpens = dict()
       for p in self.points.difference(set({point})):
           newOpens[p] = self.opens[p].difference(set({point}))
       return FiniteSpace(newOpens)
        #return FiniteSpace(nx.subgraph(self.Hasse,newNodes))
   
    def DelBeat(self,point):
        newNodes = set(self.Hasse.nodes)
        newEdges = set(self.Hasse.edges)
        newGraph = nx.DiGraph()
        newGraph.add_nodes_from(newNodes)
        newGraph.add_edges_from(newEdges)
        newGraph.remove_node(point)
        
        for p in nx.ancestors(self.Hasse,point):
            for q in nx.descendants(self.Hasse,point):
                newGraph.add_edge(p,q)
        newGraph = nx.transitive_reduction(newGraph)
        return FiniteSpace(newGraph)
        

    # Probably gets the core of a finite space
    # by randomly removing beat points
    def getCore(self):
        core = self.copy()
        (y,p) = core.hasGetBeat()
        while(y):
            core = core.delBeat(p)
            (y,p) = core.hasGetBeat()
        return core

    # Determines if a space is contractible
    def isContractible(self):
        return len(self.getCore().points)==1

    # Returns a SET of the maximal elements of a SPACE
    def getMaxs(self):
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
                candidate = nextNextSet
        return candidate

    # Given a list of elements of a space,
    # it returns the union of their downsets
    def get_Opens(self,maxs):
        newSet = FiniteSpace(dict())
        for m in maxs:
            newSet = newSet.union(self.getDownset(m))
        return newSet
    
    # This is the dummy method that I'm fiddling with
    def getOpens(self,elts):
        newElts = set(elts)
        for e in elts:
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
        nx.draw(self.Hasse,pos, with_labels = True, node_color = 'purple', font_color = 'white', font_weight = 'bold')
            