import networkx as nx
from build_knowledge_graph import KnowledgeGraph
from util import get_instinctive_activations

def main():
	graph = KnowledgeGraph().build_graph()
	while(True):
		instinctive_reactions = {}
		sensory_inputs = input("Enter your sensory inputs: \n")
		if sensory_inputs=="exit":
			break

		sensory_inputs = sensory_inputs.strip().split(' ')
		for sensory_input in sensory_inputs:
			activations = get_instinctive_activations(sensory_input, graph)
			instinctive_reactions.update(activations)

		print("Instinctive Reactions: \n", instinctive_reactions)


if __name__ == "__main__":
	main()