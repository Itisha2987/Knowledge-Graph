import networkx as nx
from build_knowledge_graph import KnowledgeGraph

def get_instinctive_activations(node, graph):
    '''
        Returns instinctive activations
        and emotional arousals from a node.
    '''
    activations = {}
    successor = list(graph.successors(node))
    
    for s in successor:
        edge_weight = int(graph[node][s]['weight'])

        # Edge weight 0 implies emotional arousal and weight 1 implies activation.
        if edge_weight == 0 or edge_weight == 1:
            activations[s] = edge_weight

    return activations


if __name__=="__main__":
    graph = KnowledgeGraph()
    kn_graph = graph.build_graph()

    activations = get_instinctive_activations('tangy_smell', kn_graph)
    print(activations)
