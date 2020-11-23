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


def get_observations(node,graph):
    '''
        Returns list of possible inferences
        and deductions from the given node,
        usign bfs traversal.
    '''

    # Set level of traversal as 2.
    level = 2
    queue = []
    queue.append(node)
    observations = {}
    l = 1

    while queue:
        if l > level:
            return observations
        size = len(queue)

        for i in range(size):
            n = queue.pop(0)
            for s in list(graph.successors(n)):
                edge_weight = int(graph[n][s]['weight'])
                # edge weight 2 implies inference while edge weight 3 implies deductions.
                if edge_weight == 2 or edge_weight == 3:
                    queue.append(s)
                    # add observation if not already included or is an inference.
                    if s not in observations or observations[s] == 2:
                        observations[s] = int(graph[n][s]['weight'])

        l = l+1
    return observations


if __name__=="__main__":
    graph = KnowledgeGraph()
    kn_graph = graph.build_graph()

    activations = get_instinctive_activations('tangy_smell', kn_graph)
    print(activations)
    observations = get_observations('spoon', kn_graph)
    print(observations)