# Modeling Finite Spaces
The purpose of this repository is to create a program for modeling finite topological spaces. It requires the packages NetworkX and numpy.

## Description of each file:


### FiniteSpaces_Class.py
This is the most important file. It includes a variety of methods for modeling finite topological spaces. The method FiniteSpace() can be fed a dictionary of open sets, or a directed graph representing the space's Hasse diagram. You can visualize the space using the drawHasse() method.
The class also includes methods for taking topological combinations of spaces: union, intersection, product, etc.
The end goal is to determine the Lusternik-Schnirelmann category of a finite space. As of now, this code produces an upper-bound for that value. The Lusternik-Schnirelmann category is important because it can be used in computing upper- and lower-bounds of the topological complexity of a space.

### FiniteSpace_Examples.py
This file stores some pre-built commonly used finite spaces, such as finite models of a circle, torus, and Klein bottle.

#### Example:
The following snippet of code displays the Hasse diagram of the minimal finite model of the Klein bottle, and then outputs an upper-bound for the geometric category of the space.
```
import FiniteSpace_Examples as FE
K = FE.Build_Klein()
K.drawHasse()
K.gcat()
```

### Brute_gcat.py
This file is for brute-force determining the geometric category of a finite topological space. It is used to check the accuracy of the gcat method from FiniteSpaces_Class. It is a very slow algorithm that runs in factorial time.

#### Brute_gcat Example:
This will output the minimal number of contractible open sets required to cover the minimal finite model of a torus. This number is exact and not an estimate, unline the gcat method of FiniteSpaces_Class.
```
import FiniteSpace_Examples as FE
import Brute_gcat as B
T = FE.Build_MinTorus()
B.get_brute_gcat(T)
```

### FiniteFunctions_Class.py
This file is very much in progress. It will be used to model continuous functions between finite topological spaces.
