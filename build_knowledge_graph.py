import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
    def build_graph(self):
        # Reading file containing all the edges of the graph
        edge_file = open("edges.txt","r")

        # Initializing a directed graph
        DG = nx.DiGraph()

        # Add weighted edges to the graph
        for line in edge_file:
            line.strip()
            head, tail, weight = line.split(' ')
            int(weight)
            #print(head,tail,weight)
            DG.add_weighted_edges_from([(head,tail, weight)])


        # Drawing graph as image "knowledge_graph.png"
        options = {
            'node_color': 'blue',
            'node_size': 800,
            'width': 2,
        }
        nx.draw(DG, with_labels=True,**options)
        graph_image = plt.gcf()
        graph_image.set_size_inches(18.5, 10.5)
        graph_image.savefig("knowledge_graph1.png",dpi=500)


if __name__=="__main__":
    graph = KnowledgeGraph()
    graph.build_graph()