from build_knowledge_graph import KnowledgeGraph
from util import get_instinctive_activations
from util import get_observations
from util import is_dangling_node
from util import get_parent_nodes
from util import seperate_observations_and_predictions


def main():
	graph = KnowledgeGraph().build_graph()
	instinctive_reactions = {}
	observations = {}
	predictions = {}
	object_recognized = {}
	inputs = []

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

		# adding new user inputs in inputs set
		inputs.extend(new_inputs)
		
		'''
			for new_inputs check for dangling node
			if dangling node add its parents to objects_recognized set
		'''
		for new_sensory_input in new_inputs:
			if is_dangling_node(new_sensory_input, graph):
				possible_recognitions = get_parent_nodes(new_sensory_input, graph)
				if len(object_recognitions_for_given_level) == 0:
					object_recognitions_for_given_level = possible_recognitions
				else:
					object_recognitions_for_given_level = object_recognitions_for_given_level.intersection(possible_recognitions)

		# For each input get activations, observations and predictions
		for sensory_input in inputs:
			
			# Activations
			activations = get_instinctive_activations(sensory_input, graph)
			instinctive_reactions_for_given_level.update(activations)
			instinctive_reactions.update(activations)

			# Observations
			raised_observations = get_observations(sensory_input, graph)
			observations_for_given_level.update(raised_observations)
			observations.update(raised_observations)

		# Adding old observations to input set
		inputs = list(observations_for_given_level)

		# Separating observations and predictions
		observations_for_given_level, predictions_for_given_level = seperate_observations_and_predictions(observations_for_given_level)
		
		print("\nObservations for given level: \n", observations_for_given_level)
		print("\nPredictions for given level: \n", predictions_for_given_level)
		print("\nObjects Recognized for given level: \n", object_recognitions_for_given_level)
		print("\nInstinctive Reactions for given level: \n", instinctive_reactions_for_given_level)

	print("---------------------------------------------------")
	print("Final Observations \n", observations)
	print("---------------------------------------------------")
	print("Final Predictions \n", predictions)
	print("---------------------------------------------------")
	print("Final Instinctive Reactions \n", instinctive_reactions)
	print("---------------------------------------------------")
	print("Final Object Recognized \n", object_recognized)
	print("---------------------------------------------------")


if __name__ == "__main__":
	main()
