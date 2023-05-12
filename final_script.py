from typing import List

class Node:
    def __init__(self, burned:bool, time_suppressed:int, ix:int, iy:int, next_node=None):
        self.BURNED = burned
        self.TIME_SUPPRESSED = time_suppressed
        self.IX = ix
        self.IY = iy
        self.NEXT = next_node

class Supp:
    def __init__(self, ixcen:int, iycen:int):
        self.IXCEN = ixcen 
        self.IYCEN = iycen

class ListTagged:
    def __init__(self, num_nodes:int, head:Node):
        self.NUM_NODES = num_nodes
        self.HEAD = head

def CENTROID(IT:int, LIST_TAGGED:ListTagged, SUPP:List[Supp]):
    IXCEN = 0
    IYCEN = 0
    COUNT = 0
    C = LIST_TAGGED.HEAD
    
    for i in range(1, LIST_TAGGED.NUM_NODES+1):
        if (C.BURNED):
            C = C.NEXT
            continue
        if (C.TIME_SUPPRESSED > 0):
            C = C.NEXT
            continue
        COUNT += 1
        IXCEN += C.IX
        IYCEN += C.IY
        C = C.NEXT
        
    if (COUNT == 0):
        COUNT = 1
        
    IXCEN = round(IXCEN / COUNT)
    IYCEN = round(IYCEN / COUNT)
    
    SUPP[IT-1].IXCEN = IXCEN
    SUPP[IT-1].IYCEN = IYCEN

if __name__ == "__main__":
    num_of_nodes = 5
    node1 = Node(False, 0, 10, 12)
    node2 = Node(True, 0, 9, 11)
    node3 = Node(False, 5, 11, 10)
    node4 = Node(False, 0, 15, 13)
    node5 = Node(True, 0, 12, 11)
    
    list_tagged_obj = ListTagged(num_of_nodes, node1)
    node1.NEXT = node2
    node2.NEXT = node3
    node3.NEXT = node4
    node4.NEXT = node5
    
    supp_obj = [Supp(0,0) for i in range(num_of_nodes)]
    
    CENTROID(3, list_tagged_obj, supp_obj)
    print(supp_obj[2].IXCEN, supp_obj[2].IYCEN)