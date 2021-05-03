import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    l = len(G.nodes)
    # print(G.nodes)
    
    s = min(G.nodes)
    t = max(G.nodes)

    if l <= 30:
        return solveSmall(G, s, t)
    elif l <= 50:
        return solveMedium(G, s, t)
    elif l <= 100:
        return solveLarge(G, s, t)
    

    # Small can delete 15 edges and 1 node

    # Medium can delete 50 edges and 3 nodes

    # Large can delete 100 edges and 5 nodes

def solveSmall(G, s, t):
    # Remove node and delete 15 edges
    
    # location 0 corresponds to best to remove at first iteration
    bestEdgeToRemove = []
    newGraph = G.copy()
    bestC, bestK = smallHelper(newGraph, s, t, 15, [])
    maxScore = calculate_score(G, bestC, bestK)
    # print(maxScore)
    
    for i in range(1, 16):
        newGraph = G.copy()
        k = []
        for j in range(len(bestEdgeToRemove)):
            e = bestEdgeToRemove[j]
            newGraph.remove_edge(e[0], e[1])
            k.append((e[0], e[1]))
        e = EdgeToRemove(newGraph, s, t)
        
        if e is None:
            break
        bestEdgeToRemove.append(e)
        k.append((e[0], e[1]))
        c, k = smallHelper(newGraph, s, t, 15 - i, k)
        score = calculate_score(G, c, k)
        if score > maxScore:
            bestC, bestK = c, k
    return bestC, bestK
        # print(Gp.has_edge(e[0], e[1]))
        
        


    # n = RemoveOneNode(Gp, s, t)
    # # print(n)
    # if n is not None:
    #     Gp.remove_node(n)
    #     c.append(n)
    # i = 0
    # while i < 15:
    #     e = EdgeToRemove(Gp, s, t)
    #     # print(e)
    #     if e is None:
    #         break
    #     k.append((e[0], e[1]))
    #     # print(Gp.has_edge(e[0], e[1]))
    #     Gp.remove_edge(e[0], e[1])
    #     i += 1
    # return c, k

def smallHelper(G, s, t, edgesLeft, k):
    Gp = G.copy()
    c = []
    n = RemoveOneNode(Gp, s, t)
    if n is not None:
        Gp.remove_node(n)
        c.append(n)
    i = 0
    while i < edgesLeft:
        e = EdgeToRemove(Gp, s, t)
        # print(e)
        if e is None:
            break
        k.append((e[0], e[1]))
        # print(Gp.has_edge(e[0], e[1]))
        Gp.remove_edge(e[0], e[1])
        i += 1
    return c, k


def solveMedium(G, s, t):
    Gp = G.copy()
    c = []
    k = []
    
    i = 0
    while i < 20:
        e = EdgeToRemove(Gp, s, t)
        # print(e)
        if e is None:
            break
        k.append((e[0], e[1]))
        # print(Gp.has_edge(e[0], e[1]))
        Gp.remove_edge(e[0], e[1])
        i += 1
    i = 0
    while i < 3:
        n = RemoveOneNode(Gp, s, t)
        # print(n)
        if n is None:
            break
        Gp.remove_node(n)
        c.append(n)
            
        i += 1
    return c, k

def solveLarge(G, s, t):
    c = []
    k = []
    Gp = G.copy()
    
    i = 0
    while i < 5:
        e = EdgeToRemove(Gp, s, t)
        if e is None:
            break
        print(e)
        k.append(e)
        Gp.remove_edge(e[0], e[1])
        i += 1
    i = 0
    while i < 5:
        n = RemoveOneNode(Gp, s, t)
        if n is None:
            break
        print(n)
        c.append(n)
        Gp.remove_node(n)
        i += 1
    return c, k

def EdgeToRemove(G, s, t):
    maxLenPath = -1
    edgeToRemove = None
    for edge in G.edges():
        copy = G.copy()
        copy.remove_edge(edge[0], edge[1])
        try:
            length, path = nx.single_source_dijkstra(copy, s, t)
        except:
            return None

        if length > maxLenPath:
            edgeToRemove = edge
            maxLenPath = length
        
    return edgeToRemove

def RemoveOneNode(G, s, t):
    maxLenPath = -1
    nodeToRemove = None
    for node in G.nodes():
        if node is not s and node is not t:
            
            copy = G.copy()
            copy.remove_node(node)
            try:
                length, path = nx.single_source_dijkstra(copy, s, t)
            except:
                return None
            if length > maxLenPath:
                nodeToRemove = node
                maxLenPath = length
        
    return nodeToRemove

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    print(path)
    G = read_input_file(path)
    c, k = solve(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'outputs' + path[6:-2] + 'out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/medium/*')
#     for input_path in inputs:
#         print(input_path)
#         output_path = 'outputs/medium/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
