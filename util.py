from global_repository import get_all_objects
from global_repository import convert_data_to_objects


def preprocess_input(sensory_input):
    return sensory_input.lower().replace(' ', '_')


def lie_within_the_range(intensity,head,tail,graph):
    '''
        Checks if the intensity lies within
        the threshold range.
    '''
    intensity = float(intensity)
    alpha = graph[head][tail]["alpha"]
    beta = graph[head][tail]["beta"]

    if intensity >= alpha and intensity <= beta:
        return True
    return False


def is_dangling_node(node, graph):
    '''
        Finds if a node is
        dangling( node with no outgoing edge).
    '''
    node = node.split(':')[0]
    if len(list(graph.successors(node))) == 0:
        return True
    return False


def  get_parent_nodes(node, graph):
    '''
        Returns parent nodes of a node
    '''
    node, intensity = node.split(':')
    predecessor_nodes = set(graph.predecessors(node))
    for pnode in predecessor_nodes.copy():
        if lie_within_the_range(intensity,pnode,node,graph) is False:
            predecessor_nodes.remove(pnode)

    return predecessor_nodes


def get_instinctive_activations(node, graph):
    '''
        Returns instinctive activations
        and emotional arousals from a node.
    '''
    node, intensity = node.split(':')
    activations = {}
    successor = list(graph.successors(node))
    
    for s in successor:
        edge_weight = int(graph[node][s]['weight'])

        # Edge weight 0 implies emotional arousal and weight 1 implies activation.
        if lie_within_the_range(intensity,node,s,graph) and (edge_weight == 0 or edge_weight == 1):
            activations[s] = edge_weight

    return activations


def get_observations(node, graph):
    '''
        Returns list of possible inferences
        and deductions from the given node,
        usign bfs traversal.
    '''
    node, intensity = node.split(':')
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
                if lie_within_the_range(intensity,node,s,graph) and (edge_weight == 2 or edge_weight == 3):
                    queue.append(s)
                    # add observation if not already included or is an inference.
                    if s not in observations or observations[s] == 2:
                        observations[s] = int(graph[n][s]['weight'])

        l = l+1

    return observations


def seperate_observations_and_predictions(input_observations):
    '''
        Returns list of predictions
        and observations.
    '''
    observations = {}
    predictions = {}
    for key in input_observations:
        value = input_observations[key]
        if value==2:
            predictions.update({key:value})
        else:
            observations.update({key:value})

    return observations, predictions


def get_intersection_set_of_recognitions(recognitions, possible_recognitions):
    '''
        Given the recognition set and new possible recognition set,
        this function returns the intersection amongst them.
    '''

    # If reocgnitions are None, then set possible recognitions as recognitions
    if len(recognitions) == 0:
        recognitions = possible_recognitions
    else:
        recognitions = recognitions.intersection(possible_recognitions)

    return recognitions
