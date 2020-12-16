import networkx as nx
from util import get_instinctive_activations
from util import get_observations
from util import is_dangling_node
from util import get_parent_nodes
from util import seperate_observations_and_predictions
from util import get_intersection_set_of_recognitions
from util import preprocess_name
from similarity import get_similar_elements
from global_repository import get_all_objects
from build_knowledge_graph import KnowledgeGraph


def add_new_nodes_to_graph(not_in_graph_inputs, graph):
	'''
		Inputs:
			-> not_in_graph_inputs: the set of inputs that were not in graph
			-> graph: the knowledge graph used
		
		Returns:
			-> nodes_added: the dictionary of node added as key
							and the similar object used for adding edges with similarity index as value
	'''
	nodes_added = {}
	data = get_all_objects()
	
	# Objects array
	objects = data["objects"]
	object_names = [preprocess_name(element["name"]) for element in objects]
	
	# Iterating through all inputs that are not in graph
	for node in not_in_graph_inputs:
		if node in object_names:
			# implies the node is in global repository and not in KG
			
			similar_objects = get_similar_elements(node)
			if not similar_objects:
				continue
			
			most_similar_object = similar_objects[0]
			# sample data: most_similar_object = (0.8, {"name": ...})
			most_similar_object_name = preprocess_name(most_similar_object[1]["name"])
			
			# add the new node in the graph
			graph.add_node(node)
			
			# get all successors of the already existing object
			successors = graph.successors(most_similar_object_name)
			
			# edge_attributes to store the weight, alpha, beta values of the edge
			edge_attributes = {}
			for successor in successors:
				# Add edge from new node to the successors
				graph.add_edge(node, successor)

				# Add edge_data to edge_attributes
				edge_attributes[(node, successor)] = graph.get_edge_data(most_similar_object_name, successor)
			
			nx.set_edge_attributes(graph, edge_attributes)

			# Finally append the node and its similar object, similarity_index used for adding edges
			nodes_added[node] = (most_similar_object_name, most_similar_object[0])
	
	return nodes_added

def cluster_input_based_on_senses(new_inputs, not_in_graph_inputs, input_set, graph):
	for i in range(len(new_inputs)):
		# Input Format:
		# T:hot:0.7 O:tangy_smell:0.7

		# get the sense of input (V/T/O/G/A), intensity by splitting up
		sense, new_input, intensity = new_inputs[i].split(':')
		new_input = preprocess_name(new_input)
		# Update new inputs by removing only sensory tags (still contains intensity value)
		new_inputs[i] = new_input + ':' + intensity

		if new_input not in graph:
			not_in_graph_inputs.add(new_input)
			continue
			
		if sense == 'V':
			sense = "vision"
		elif sense == 'T':
			sense = "tactile"
		elif sense == 'O':
			sense = "olfactory"
		elif sense == 'G':
			sense = "gustatory"
		elif sense == 'A':
			sense = "auditory"
		else:
			print("!! Invalid Input given !!\n")
			return

		# Add the input to corresponding sensory input set
		input_set[sense].append(new_inputs[i])

def get_activations_and_arousals(input_set, object_recognitions_for_given_level, object_recognized, graph):
	'''
			for new_inputs check for dangling node
			if dangling node add its parents to objects_recognized set
	'''
	for senses in input_set:
		sensory_level_recognition = set()
		if input_set[senses]:
			for node in input_set[senses]:
				if is_dangling_node(node, graph):
					possible_recognitions = get_parent_nodes(node, graph)
					sensory_level_recognition = get_intersection_set_of_recognitions(sensory_level_recognition, possible_recognitions)

		object_recognitions_for_given_level.update(sensory_level_recognition)

	# Update the object recognized
	object_recognized.update(object_recognitions_for_given_level)

def main():
	graph = KnowledgeGraph().build_graph()
	instinctive_reactions = {}
	observations = {}
	predictions = {}
	object_recognized = set()
	inputs = []
	not_in_graph_inputs = set()

	while(True):

		# Take User Input until user enters exit	
		sensory_inputs = input("\nEnter your sensory inputs: \n")
		if sensory_inputs=="exit":
			break

		observations_for_given_level = {}
		predictions_for_given_level = {}
		instinctive_reactions_for_given_level = {}
		object_recognitions_for_given_level = set()

		# new_inputs the user has entered
		new_inputs = sensory_inputs.strip().split(' ')
		
		# Divide new sensory inputs into different afferent (sensory) groups.
		input_set = {
			"auditory": [],
			"gustatory": [],
			"tactile": [],
			"olfactory": [],
			"vision": []
		}
		
		cluster_input_based_on_senses(new_inputs, not_in_graph_inputs, input_set, graph)
		get_activations_and_arousals(input_set, object_recognitions_for_given_level, object_recognized, graph)

		# getting elements to be removed
		elements_to_be_removed = []
		for elem in new_inputs:
			input_name = elem.split(':')[0]
			if input_name in not_in_graph_inputs:
				elements_to_be_removed.append(elem)

		# Removing elements from new_inputs
		for elem in elements_to_be_removed:
			new_inputs.remove(elem)
		
		# adding new user inputs in inputs set
		inputs.extend(new_inputs)

		# For each input get activations, observations and predictions
		for sensory_input in inputs:

			# Activations
			activations = get_instinctive_activations(sensory_input, graph)
			instinctive_reactions_for_given_level.update(activations)
			instinctive_reactions.update(activations)

			# Observations
			raised_observations = get_observations(sensory_input, graph)
			observations_for_given_level.update(raised_observations)

		# Adding old observations to input set
		# TODO. Need to figure out proper way for appending threshold value
		inputs = [observation+":1" for observation in list(observations_for_given_level)]

		# Separating observations and predictions and updating their final set
		observations_for_given_level, predictions_for_given_level = seperate_observations_and_predictions(observations_for_given_level)
		observations.update(observations_for_given_level)
		predictions.update(predictions_for_given_level)

		if observations_for_given_level:
			print("\nObservations for given level: \n", observations_for_given_level)
		if predictions_for_given_level:
			print("\nPredictions for given level: \n", predictions_for_given_level)
		if object_recognitions_for_given_level:
			print("\nObjects Recognized for given level: \n", object_recognitions_for_given_level)
		if instinctive_reactions_for_given_level:
			print("\nInstinctive Reactions for given level: \n", instinctive_reactions_for_given_level)

	if observations:
		print("---------------------------------------------------")
		print("Final Observations \n", observations)
	if predictions:
		print("---------------------------------------------------")
		print("Final Predictions \n", predictions)
	if instinctive_reactions:
		print("---------------------------------------------------")
		print("Final Instinctive Reactions \n", instinctive_reactions)
	if object_recognized:
		print("---------------------------------------------------")
		print("Final Object Recognized \n", object_recognized)
	print("---------------------------------------------------")

	nodes_added = add_new_nodes_to_graph(list(not_in_graph_inputs), graph)
	if nodes_added:
		print("The following nodes were added into the knowledge graph using the given similarity:")
		print(nodes_added)


if __name__ == "__main__":
	main()
