from typing import List

class Node:
    def __init__(self, IX: int, IY: int, TIME_SUPPRESSED: float, BURNED: bool, NEXT):
        self.IX = IX
        self.IY = IY
        self.TIME_SUPPRESSED = TIME_SUPPRESSED
        self.BURNED = BURNED
        self.NEXT = NEXT

class Supp:
    def __init__(self):
        self.IXCEN = 0
        self.IYCEN = 0

class ListTagged:
    def __init__(self):
        self.NUM_NODES: int = 0
        self.HEAD: Node = None

SUPP: List[Supp] = [Supp() for i in range(10)]
LIST_TAGGED = ListTagged()

def Centroid(IT: int):
    global LIST_TAGGED, SUPP
    
    IXCEN = 0
    IYCEN = 0
    COUNT = 0
    C = LIST_TAGGED.HEAD
    
    for i in range(LIST_TAGGED.NUM_NODES):
        if C.BURNED:
            C = C.NEXT
            continue
        if C.TIME_SUPPRESSED > 0.:
            C = C.NEXT
            continue
        
        COUNT += 1
        IXCEN += C.IX
        IYCEN += C.IY
        C = C.NEXT
        
    if COUNT == 0:
        COUNT = 1
    IXCEN = round(IXCEN/COUNT)
    IYCEN = round(IYCEN/COUNT)
    
    SUPP[IT-1].IXCEN = IXCEN
    SUPP[IT-1].IYCEN = IYCEN

if __name__ == '__main__':
    # define and initialize the variables used in the code
    node1 = Node(10, 20, 0.1, False, None)
    node2 = Node(20, 30, 0.0, False, node1)
    node3 = Node(30, 40, 0.2, False, node2)
    LIST_TAGGED.NUM_NODES = 3
    LIST_TAGGED.HEAD = node3
    IT = 1
    
    # call the Centroid function
    Centroid(IT)
    
    # print the values of SUPP[0].IXCEN and SUPP[0].IYCEN
    print(SUPP[0].IXCEN)
    print(SUPP[0].IYCEN)