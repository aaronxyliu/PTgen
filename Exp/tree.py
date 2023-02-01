### Basic tree usage example


from ete3 import Tree

t = Tree() # Creates an empty tree
A = t.add_child(name="A") # Adds a new child to the current tree root
                           # and returns it
B = t.add_child(name="B") # Adds a second child to the current tree
                           # root and returns it
C = A.add_child(name="C") # Adds a new child to one of the branches
D = C.add_sister(name="D") # Adds a second child to same branch as
                             # before, but using a sister as the starting
                             # point
R = A.add_child(name="R") # Adds a third child to the
                           # branch. Multifurcations are supported


C= t&"C"
D= t&"D"
R= t&"R"

# Let's now add some custom features to our nodes. add_features can be
# used to add many features at the same time.
C.add_features(vowel=False, confidence=1.0)
D.add_features(vowel=True, confidence=0.5)

print(t.get_ascii(show_internal=True))
print(t.write(features=["vowel", "confidence"],format=1))
print(t.name)