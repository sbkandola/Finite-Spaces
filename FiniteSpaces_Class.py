# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:12:47 2020

@author: Shelley
"""

class FiniteSpace:

    # Some built-in spaces... is there a better way to do this?
        # I want something like "FS.S1" to be a built-in model of S1
    S1 = dict({'a': set({'a','c','d'}),
       'b': set({'b','c','d'}), 
       'c': set({'c'}), 
       'd': set({'d'})})
    
    # 6-point model of S1
    S13 = dict({
        'y0': set({'y0','x0','x1'}),
        'y1': set({'y1','x1','x2'}),
        'y2': set({'y2','x2','x0'}),
        'x0': set({'x0'}),
        'x1': set({'x1'}),
        'x2': set({'x2'})
    })
    
    # 10-point model of S1
    S15 = dict({
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
    })    
    
    # Minimal finite model of Klein bottle
    K = dict({
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
        'c4': set({'c4'})})

    
    # Pass in a number k to generate a k-point model of [0,1]
    def __init__(self, opens=dict(), k=0):
        self.opens = opens
        self.points = set(opens.keys())
        self.closures = dict()
        
        if k > 0:
            for i in range(k):
                if i%2==0:
                    self.opens[str(i)] = set({str(i)})
                else:
                    self.opens[str(i)] = set({str(max(i-1,0)),str(i),str(min(i+1,k-1))})
                    
                    
        
    def __len__(self):
         return len(self.points)
     
        
    
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
    
    # copies a finite space
    def copy(self):
        newSet = dict()
        for p in self.opens:
            newSet[p] = set(self.opens[p])
        return FiniteSpace(newSet)
     
    # returns the union of self with another space
    def union(self,space2):
        union = self.copy()
        for p in set(space2.opens).difference(set(self.opens)):
            union.opens[p] = set(space2.opens[p])
        union.points = set(union.opens.keys())
        return union
    
    def intersection(self, space2):
        intersection = FiniteSpace(dict())
        for p in set(self.points).intersection(set(space2.points)):
            intersection[p] = set(self.opens[p])
        intersection.points = set(intersection.opens.keys())
        return FiniteSpace(intersection)
    
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

    def getDownset(self,point):
        if point not in self.opens:
            print(point+' is not in space.')
        downset = dict()
        for p in self.opens[point]:
            downset[p] = self.opens[p]
        return FiniteSpace(downset)
    
    def getPuncturedDownset(self,point):
        puncturedDownset = dict()
        for p in self.opens[point].difference(set({point})):
            puncturedDownset[p] = self.opens[p].difference(point)
        return FiniteSpace(puncturedDownset)
            
    
    def getUpset(self,point):
        if len(self.closures)==0:
            self.getClosures()
        if point not in self.opens:
            print(point+' is not in space.')
        upset = dict()
        for p in self.closures[point]:
            upset[p] = self.opens[p]
        return FiniteSpace(upset)
    
    def getPuncturedUpset(self,point):
        if len(self.closures)==0:
            self.getClosures()
        puncturedUpset = dict()
        for p in self.closures[point].difference(set({point})):
            puncturedUpset[p] = self.opens[p].difference(point)
        return FiniteSpace(puncturedUpset)
        
    
    def hasUniqueMax(self):
        if not self.isT0:
                return False
        if len(self.opens)==1:
            return True
        for p in self.opens:
            if self.opens[p]==self.points:
                return True
        return False    

    # Returns the unique maximal element of a set
    def getUniqueMax(self):
        if self.hasUniqueMax():
            if len(self.opens)==1:
                return self.opens
            for p in self.opens:
                if self.opens[p]==self.points:
                    return p
        print('no unique max elt')
        return
    
    # Determines if a space has a unique minimal element
    def hasUniqueMin(self):
        if len(self.points)==0:
            return False
        if len(self.closures)==0:
            self.getClosures()
        if len(self.points)==1:
            return True
        for p in self.points:
            # If a point's closure contains the whole space
            if self.closures[p]==self.points:
                return True
        return False
    
    # Returns the unique minimal element of a set 
    def getUniqueMin(self):
        if len(self.points)==0:
            return False
        if len(self.closures)==0:
            self.getClosures()
        if self.hasUniqueMin():
            for p in self.points:
                if self.closures[p]==self.points:
                    return p

    def isBeat(self,point):
        test1 = self.getPuncturedDownset(point).hasUniqueMax()
        test2 = self.getPuncturedUpset(point).hasUniqueMin()
        return (test1|test2)
    
    def hasBeat(self):
        for p in self.points:
            if self.isBeat(p):
                return True
        
    # How can I control the randomness of this method?
    def getBeat(self):
        for p in self.points:
            if self.isBeat(p):
                return p
            
    def hasGetBeat(self):
        for p in self.points:
            if self.isBeat(p):
                return (True,p)
        return (False,'')
        
            
    def delBeat(self,point):
        newOpens = dict()
        for p in self.points.difference(set({point})):
            newOpens[p] = self.opens[p].difference(set({point}))
        return FiniteSpace(newOpens)
    
    def getCore(self):
        core = self.copy()
        (y,p) = core.hasGetBeat()
        while(y):
            core = core.delBeat(p)
            (y,p) = core.hasGetBeat()
        return core
    
    def isContractible(self):
        return len(self.getCore().points)==1
    
    # Returns a SET of the maximal elements of a SPACE
    def getMaxs(self):
        maxs = set()
        for p in self.points:
            if len(self.getUpset(p).points)==1:
                maxs.add(p)
        return maxs
    
    # Greedy algorithm builds the largest contratctible subset
    # # of a space that it can by randomly adding other downsets
    def buildMaxContractible(self):
        maxs = self.getMaxs()
        candidate = self.getDownset(maxs.pop())
        while len(maxs)>0:
            nextSet = self.getDownset(maxs.pop())
            if candidate.union(nextSet).isContractible():
                candidate = candidate.union(nextSet)
        return candidate
    
    # Given a list of elements of a space, 
    # it returns the union of their downsets
    def getOpens(self,maxs):
        newSet = FiniteSpace(dict())
        for m in maxs:
            newSet = newSet.union(self.getDownset(m))
        return newSet
    
    # Estimates the gcat of a space
    def gcat(self):
        maxs = self.getMaxs()
        gc = 0
        while len(maxs)>0:
            usedMaxs = self.getOpens(maxs).buildMaxContractible().getMaxs()
            print(maxs)
            maxs.difference_update(usedMaxs)
            gc = gc + 1
        return gc
    
    
            
            