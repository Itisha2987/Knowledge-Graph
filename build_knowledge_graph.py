import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
    def build_graph(self):
        # Reading file containing all the edges of the graph
        edge_file = open("edges.txt","r")

        # Initializing a directed graph
        DG = nx.DiGraph()

        # Add weighted edges to the graph
        threshold_attributes = {}
        for line in edge_file:
            line = line.strip('\n')
            head, tail, weight, alpha, beta = line.split(' ')
            int(weight)
            float(alpha)
            float(beta)
            DG.add_weighted_edges_from([(head,tail, weight)])

            # alpha - Minimum threshold of an edge
            # beta  - Maximum threshold of an edge
            threshold_attributes[(head, tail)] = {"alpha":alpha,"beta":beta}


        # Adding Threshold attributes of each edge to the graph
        nx.set_edge_attributes(DG, threshold_attributes)

        # Testing Alpha-Beta Values
        # print("Water-Liquid\nAlpha: " + str(DG["water"]["liquid"]["alpha"]) + "\nBeta: " + str(DG["water"]["liquid"]["beta"]))
        # print("Water-Liquid\nAlpha: " + str(DG["bowl"]["has_rim"]["alpha"]) + "\nBeta: " + str(DG["bowl"]["has_rim"]["beta"]))
        
        # Drawing graph as image "knowledge_graph.png"
        options = {
            'node_color': 'blue',
            'node_size': 800,
            'width': 2,
        }
        nx.draw(DG, with_labels=True,**options)
        graph_image = plt.gcf()
        graph_image.set_size_inches(18.5, 10.5)
        graph_image.savefig("knowledge_graph.png",dpi=500)

        return DG
