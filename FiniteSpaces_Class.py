# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:12:47 2020

@author: Shelley
"""

import networkx as nx
import numpy as np
import operator
import random


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
            self.adjacencies = nx.Graph()
            for v in self.points:
                for u in nx.descendants(self.Hasse, v):
                    self.adjacencies.add_edge(v, u)

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
            self.adjacencies = nx.Graph()
            for v in self.points:
                for u in nx.descendants(inputData, v):
                    self.adjacencies.add_edge(v, u)

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
        There is an error somewhere in here!
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
        return (p2 in self.Hasse.successors(p1) or p1==p2)

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
        return (p1 in self.Hasse.successors(p2) or p1==p2)

    def product(self, space2):
        '''


        Parameters
        ----------
        space2 : FiniteSpace
            A FiniteSpace whose point names do not already contain commas.
            If self != space2, the points should have DIFFERENT NAMES.

        Returns
        -------
        FiniteSpace
            The product of self with space2.

        '''
        s1xs2 = nx.DiGraph()
        prod = []
        for p in self.points:
            for q in space2.points:
                prod.append(p+','+q)
        s1xs2.add_nodes_from(prod)

        for pair in prod:
            points = pair.rsplit(',',1)
            for p in self.getDownset(points[0]).points:
                for q in space2.getDownset(points[1]).points:
                    target = p+','+q
                    if pair != target:
                        s1xs2.add_edge(pair,target)
        s1xs2 = nx.transitive_reduction(s1xs2)

        return FiniteSpace(s1xs2)


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
            space2 is the "top" space

        '''
        if set(self.points).isdisjoint(set(space2.points)):
            join = self.union(space2)
            for q in space2.opens:
                for p in self.opens:
                    join.opens[q].add(p)
        return join


    def randomize(self, prob, connected):
        randomSpace = nx.DiGraph()

        for p in self.points:
            for q in self.points:
                if (p!=q) and (random.random() < prob):
                    randomSpace.add_edge(p,q)
                    if nx.is_weakly_connected(randomSpace)==connected:
                        try:
                            nx.find_cycle(randomSpace)
                            randomSpace.remove_edge(p, q)
                        except:
                            pass
        randomSpace = nx.transitive_reduction(randomSpace)

        return FiniteSpace(randomSpace)



    def isOpen(self):
        '''
        Returns
        -------
        True if self is a union of open sets

        '''
        for p in self.points:
            pDown = self.getDownset(p)
            for q in pDown.points:
                qDown = self.getDownset(q)
                if not(set(qDown.points).issubset(set(self.points))):
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

    def isConnected(self):
        '''
        Determines if a FiniteSpace is path-connected

        Returns
        -------
        True if self is connected. False otherwise.

        '''
        return(nx.is_weakly_connected(self.Hasse))

    def getPath(self,a,b):
        '''


        Parameters
        ----------
        a : string
            a point of a FiniteSpace.
        b : string
            a point of a FiniteSpace.

        Returns
        -------
        list containing a zigzag of points from a to b.

        '''
        return(nx.shortest_path(self.adjacencies, a, b))


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
        downnodes = downnodes.union(set({point}))
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

    def beatRetract(self,point):
        '''


        Parameters
        ----------
        point : STRING
            Name of a point in a FiniteSpace.

        Returns
        -------
        None.

        '''
        upbeat = self.Hasse.in_degree(point)==1
        downbeat = self.Hasse.out_degree(point)==1

        if downbeat:
            down = list(self.Hasse.successors(point))[0]
            return down
        elif upbeat:
            up = list(self.Hasse.predecessors(point))[0]
            return up


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
        upbeat = self.Hasse.in_degree(point)==1
        downbeat = self.Hasse.out_degree(point)==1
        return (upbeat|downbeat)

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

    def hasGetBeatRetract(self):
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
                return (True,p,self.beatRetract(p))
        return (False,'','')


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


    def getRetract(self):
        '''


        Returns
        -------
        deformation : LIST
            A list of ordered pairs of points (p,q) of self
            where p is a beat point and q is the image of p
            under a deformation retract.

        '''
        deformation = list()
        core = self
        (y,p,q) = core.hasGetBeatRetract()
        while(y):
            deformation.append((p,q))
            core = core.delBeat(p)
            (y,p,q) = core.hasGetBeatRetract()
        return deformation

    def hasGet2Chain(self):
        for m in self.getMaxs():
            if len(self.getPuncturedDownset(m))>0:
                for n in self.Hasse.successors(m):
                    if len(self.getPuncturedDownset(n))>0:
                        return (True,n)
                    else:
                        return (False,'')


    def getCatPath(self,a):
        '''


        Parameters
        ----------
        a : String
            The name of a point in self.

        Returns
        -------
        path_space : FiniteSpace
            If self is contractible, this returns a zigzag
            whose endpoints are 'a' and the core of self
            as a FiniteSpace.

        '''
        if len(self.getCore())!=1:
            print("Space is not contractible.")
            return
        else:
            deformation = self.getRetract()
            core = deformation[len(deformation)-1][1]
            path = list()
            path.append(a)
            while core not in path:
                last = path[len(path)-1]
                next_point = [pair[1] for pair in deformation if pair[0]==last][0]
                path.append(next_point)
            print(path)
            path_space = FiniteSpace(self.Hasse.subgraph(set(path)))
            (y,p) = path_space.hasGet2Chain()
            while y:
                path_space = path_space.delBeat(p)
                (y,p) = path_space.hasGet2Chain()


            return path_space


    def getMotionPlanner(self,ab_cover,a,b):
        '''


        Parameters
        ----------
        cover : FiniteSpace
            A categorical subset of self^2 containing
            the point (a,b).
        a : String
            The name of a start point in self.
        b : String
            The name of an end point in self.

        Returns
        -------
        None.

        '''
        ab = str(a+','+b)
        if ab not in ab_cover.points:
            print(str(ab)+str(" is not in space."))

        print("Core is "+str(ab_cover.getCore().points))

        deformation = ab_cover.getRetract()
        core = deformation[len(deformation)-1][1]
        core_a = core.rsplit(',',1)[0]
        core_b = core.rsplit(',',1)[1]
        path = list()
        path.append(ab)


        for pair in deformation:
            last = path[len(path)-1]
            if pair[0]==last:
                path.append(pair[1])
            else:
                path.append(last)

        print(path)

        ab_path = list()

        # Follow the path to the core
        for i in range(len(path)):
            ab_path.append(path[i].rsplit(',',1)[0])

        # Path between two points of core
        core_path = self.getPath(core_a,core_b)
        ab_path = ab_path + core_path[1:len(core_path)-1]

        # Path from core to end?
        # TODO This is where I'm at! Is the indexing right?!??
        for i in range(len(path)):
            ab_path.append(path[len(path)-i-1].rsplit(',',1)[1])
        return(ab_path)



    def getCore_old(self):
        '''
        Returns
        -------
        core : FiniteSpace
            A space homotopy equivalent to self that has no beat points.

        '''
        core = self
        (y,p) = core.hasGetBeat()
        # print(p)
        while(y):
            core = core.delBeat(p)
            (y,p) = core.hasGetBeat()
            #print(p)
        return core
    
    def getVertexLists(self,G):
        L_in = []
        L_out = []
        for v in G.nodes():
            indeg = G.in_degree(v)
            outdeg = G.out_degree(v)
            if indeg>0: # Don't add maximal elements
                L_in.append(  (indeg, v)  )
            if outdeg>0: # Don't add minimal elements
                L_out.append( (outdeg, v))
        L_in.sort()
        L_out.sort()
        
        return L_in,L_out
    
    def getCore(self):
        G = nx.DiGraph(self.Hasse)
        L_in,L_out = self.getVertexLists(G)
        while (len(L_in)>0 and L_in[0][0] ==1) or (len(L_out)>0 and L_out[0][0] ==1):
            # if a vertex has in-degree 1
            if L_in[0][0] ==1:
                # get that vertex
                First = L_in.pop(0)
                p = First[1]
                
                # Get the only upper neighbor
                w = next(G.predecessors(p))
                # Get all the lower neighbors
                U = [u for u in G.successors(p)]
                
                # Remove that vertex
                G.remove_node(p)
                
                # Add all the edges that would've been deleted
                edges = [(w,u) for u in U]
                G.add_edges_from(edges)
                
                # Remove excess edges
                G = nx.transitive_reduction(G)
                
                # Recreate the vertex lists
                L_in,L_out = self.getVertexLists(G)
                
                
                
                
            elif L_out[0][0] ==1:
                First = L_out.pop(0)
                p = First[1]
                
                # Get the only lower neighbor
                w = next(G.successors(p))
                # Get all the upper neighbors
                U = [u for u in G.predecessors(p)]
                
                # Remove the vertex
                G.remove_node(p)
                
                # Replace the edges
                edges = [(u,w) for u in U]
                G.add_edges_from(edges)
                G = nx.transitive_reduction(G)
                
                L_in,L_out = self.getVertexLists(G)
                
        return(FiniteSpace(G))

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
        Determines if self is a disjoint union of contractible sets

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
        '''
        Gets the maximal elements of a space.

        Returns
        -------
        maxs : list
            A list of strings that are the names of the maximal elements of self.

        '''
        if not self.Hasse:
            self.getHasse()
        maxs = set(n for n in self.Hasse.nodes if self.Hasse.in_degree(n)==0)
        return maxs


    def getCatCover(self, verbose=False):
        '''
        Approximates the geometric category of a finite space

        Returns
        -------
        maxCover : list
            Returns a list of finite spaces whose union covers self.

        '''
        maxCover = []
        maxs = self.getMaxs()
        if verbose:
            print('maxs are ', maxs)
        m = maxs.pop()
        maxCover.append(self.getDownset(m))
        # This approach doesn't work if the space isn't path-connected
        dist_dict = nx.shortest_path_length(self.adjacencies, m)
        sorted_dict = sorted(dist_dict.items(), key=operator.itemgetter(1))
        sorted_maxs = [key[0] for key in sorted_dict if key[0] in maxs]
        for m in sorted_maxs:
            found = False
            nextMax = self.getDownset(m)
            for c in range(len(maxCover)):
               testUnion = maxCover[c].union(nextMax)
               # ToDo: we can only allow contractible components if the ambient space is path connected
               if (testUnion.isContractibleComponents()):
                   maxCover[c] = testUnion
                   found = True
                   break
            if found==False:
                maxCover.append(nextMax)
        return maxCover


    def shuffleCatCover(self, randomizeStart = True, randomizeStyle = "BFS", verbose = False):
        '''
        Approximates the geometric category of a finite space

        randomizeStart: boolean
            If true, the starting cover element is chosen randomly
            If False, it is the first element popped from the max list
            Note that if randomizeStyle is "Random", then this has no effect.

        randomizeStyle: string
            If "Random", then it shuffles all maximal elements without regards to distance
            If "BFS", then it sorts the elements in BFS order,
            If "BFS-random", also shuffles within the elements of the same distance.

        Returns
        -------
        maxCover : list
            Returns a list of finite spaces whose union covers self.

        '''
        maxCover = []
        maxs = list(self.getMaxs())


        if "BFS" in randomizeStyle.upper():
            # Find the BFS ordering from a starting element,
            if randomizeStart:
                index = np.random.randint(len(maxs))
            else:
                index = 0
            m = maxs.pop(index)
            maxCover.append(self.getDownset(m))

            if verbose:
                print("Using BFS")
                print("Starting max is "+str(m))

            # Sort the elements based on distance to the initial max element
            dist_dict = nx.shortest_path_length(self.adjacencies, m)
            dict_by_distance = {}
            for u in maxs:
                dist = dist_dict[u]
                if dist in dict_by_distance.keys():
                    dict_by_distance[dist].append(u)
                else:
                    dict_by_distance[dist] = [u]

            dists = list(dict_by_distance.keys())
            dists.sort()

            # Shuffle each distance list if randomizeStyle is "BFS-Random"
            if "RANDOM" in randomizeStyle.upper():
                if verbose:
                    print("Using random BFS")
                for key in dict_by_distance.keys():
                    np.random.shuffle(dict_by_distance[key])


            sorted_maxs = np.concatenate([dict_by_distance[i] for i in dists])

            if verbose:
                print("sorted maxes are",sorted_maxs)

        if randomizeStyle.upper() == "RANDOM":
            # Randomize by just randomizing the list of maximal elements

            sorted_maxs = maxs
            np.random.shuffle(sorted_maxs)

            # Initialize the cover with a single element
            index = np.random.randint(len(maxs))
            m = sorted_maxs.pop(index)
            maxCover.append(self.getDownset(m))


        for m in sorted_maxs:
            #print('working on m =',m)
            #print('Current cover list is ', [ cover.getMaxs() for cover in maxCover])
            found = False
            nextMax = self.getDownset(m)
            for c in range(len(maxCover)):
               testUnion = maxCover[c].union(nextMax)
               #if (testUnion.isContractibleComponents() or nextMax.hasEmptyIntersection(maxCover[c])):
               if (testUnion.isContractibleComponents()):
                   #print(m + " union "+str(maxCover[c].getMaxs()) + " is contractible.")
                   maxCover[c] = testUnion
                   found = True
                   break
            if found==False:
                #print(m + " union "+str(maxCover[c].getMaxs()) + " is NOT contractible.")
                maxCover.append(nextMax)
            #print('Current cover list is ', [ cover.getMaxs() for cover in maxCover])
        return maxCover



    # returns the union of downsets of a list of elements
    def getOpens(self,elts):
        newElts = set(elts)
        #newElts = set()
        for e in elts:
            newElts = newElts.union(set(nx.descendants(self.Hasse,e)))
        return FiniteSpace(self.Hasse.subgraph(newElts))


    # Estimates the gcat of a space
    def LScat(self):
        return len(self.getCatCover())

    # gets the height of a point in a Hasse diagram
    def getHeight(self,point):
        if len(self.Hasse)==0:
            self.getHasse()
        return len(nx.dag_longest_path(nx.dfs_tree(self.Hasse,point)))-1

    # gets the dimension of the space
    def getDim(self):
        dim = 0
        for m in self.getMaxs():
            dim = max(dim, self.getHeight(m))
        return dim

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
        nx.draw(self.Hasse,pos, with_labels = True, node_size = 500, node_color = 'orange', font_color = 'teal', font_weight = 'bold')
