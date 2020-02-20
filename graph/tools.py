import numpy as np
import networkx as nx


def edge2mat(link, num_node):
    A = np.zeros((num_node, num_node))
    for i, j in link:
        A[j, i] = 1
    return A


def centrality_adjacency(A):
    Dl = np.sum(A, 0)
    G=nx.from_numpy_matrix(A)
    centrality = nx.closeness_centrality(G)
    num_node = A.shape[0]
    for i in range(num_node):
        for j in range(num_node):
            if Dl[i] > 0:
                A[i, j] = centrality.get(j)
    return A

def normalize_digraph(A):
    A = centrality_adjacency(A)
    Dl = np.sum(A, 0)  
    num_node = A.shape[0]
    Dn = np.zeros((num_node, num_node))
    for i in range(num_node):
        for j in range(num_node):
            if Dl[i] > 0:
                A[i, j] = A[i, j]*((Dl[i]-1)+1)
    Dl = np.sum(A, 0)
    for i in range(num_node):
        if Dl[i]>0:
            Dn[i, i] = Dl[i]**(-1)
    AD = np.dot(A, Dn)
    return AD


def get_spatial_graph(num_node, self_link, inward, outward):
    I = edge2mat(self_link, num_node)
    In = normalize_digraph(edge2mat(inward, num_node))
    Out = normalize_digraph(edge2mat(outward, num_node))
    A = np.stack((I, In, Out))
    return A
