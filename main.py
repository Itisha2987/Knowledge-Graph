from build_knowledge_graph import KnowledgeGraph
from util import get_instinctive_activations
from util import get_observations
from util import is_dangling_node
from util import get_parent_nodes
from util import seperate_observations_and_predictions
from util import get_intersection_set_of_recognitions


def main():
	graph = KnowledgeGraph().build_graph()
	instinctive_reactions = {}
	observations = {}
	predictions = {}
	object_recognized = set()
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
		
		# Divide new sensory inputs into different afferent (sensory) groups.
		input_set = {
			"auditory": [],
			"gustatory": [],
			"tactile": [],
			"olfactory": [],
			"vision": []
		}
		
		for i in range(len(new_inputs)):
			# get the sense of input (V/T/O/G/A)
			sense, new_input, intensity = new_inputs[i].split(':')

			# Update new inputs by removing sensory tags
			new_inputs[i] = new_inputs[i][2:]
			
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
		

		'''
			for new_inputs check for dangling node
			if dangling node add its parents to objects_recognized set
		'''
		for senses in input_set:
			sensory_level_recognition = set()
			if input_set[senses]:
				for node in input_set[senses]:
					node = node.split(':')[0]
					if is_dangling_node(node, graph):
						possible_recognitions = get_parent_nodes(node, graph)
						sensory_level_recognition = get_intersection_set_of_recognitions(sensory_level_recognition, possible_recognitions)

			object_recognitions_for_given_level.update(sensory_level_recognition)

		# Update the object recognized
		object_recognized.update(object_recognitions_for_given_level)


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
		# inputs = list(observations_for_given_level)
		inputs = [observation+":1" for observation in list(observations_for_given_level)]

		# Separating observations and predictions and updating their final set
		observations_for_given_level, predictions_for_given_level = seperate_observations_and_predictions(observations_for_given_level)
		observations.update(observations_for_given_level)
		predictions.update(predictions_for_given_level)

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
