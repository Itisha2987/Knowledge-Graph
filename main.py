from build_knowledge_graph import KnowledgeGraph
from util import get_instinctive_activations
from util import get_observations


def main():
	graph = KnowledgeGraph().build_graph()
	instinctive_reactions = {}
	observations_and_predictions = {}
	final_results = {}
	inputs = []
	visited_nodes = []
	while(True):
		sensory_inputs = input("\nEnter your sensory inputs: \n")
		if sensory_inputs=="exit":
			break

		observation_for_given_level = {}
		instinctive_reactions_for_given_level = {}
		results_for_given_level = {}

		inputs.extend(sensory_inputs.strip().split(' '))
		for sensory_input in inputs:
			if sensory_input in visited_nodes:
				continue
			activations = get_instinctive_activations(sensory_input, graph)
			instinctive_reactions_for_given_level.update(activations)
			instinctive_reactions.update(activations)
			observations, results = get_observations(sensory_input, graph)
			# print(observations)
			results_for_given_level.update(results)
			final_results.update(results)
			observation_for_given_level.update(observations)
			observations_and_predictions.update(observations)

		inputs = list(observation_for_given_level)

		print("Observations for given level: \n", observation_for_given_level)
		print("Results for given level: \n", results_for_given_level)
		print("Instinctive Reactions for given level: \n", instinctive_reactions_for_given_level)

	print("---------------------------------------------------")
	print("Final Observations \n", observations_and_predictions)
	print("---------------------------------------------------")
	print("Final Instinctive Reactions \n", instinctive_reactions)
	print("---------------------------------------------------")
	print("Final Results \n", final_results)
	print("---------------------------------------------------")


if __name__ == "__main__":
	main()
