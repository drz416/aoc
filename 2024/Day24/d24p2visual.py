from pathlib import Path
from pprint import pprint


import networkx as nx
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def visualize_graph_pyqt(graph_data):
  """
  Creates a visualization of a network graph using PyQt5.

  Args:
    graph_data: A list of tuples representing the edges of the graph. 
                Each tuple should contain two nodes connected by an edge.
                Example: [('A', 'B'), ('B', 'C'), ('A', 'C')]
  """

  # Import matplotlib.pyplot within the function
  import matplotlib.pyplot as plt

  # Create a NetworkX graph object
  G = nx.Graph()

  # Add edges to the graph
  G.add_edges_from(graph_data)

  # Create a matplotlib figure
  fig, ax = plt.subplots()
  pos = nx.spring_layout(G) 
  nx.draw(G, pos, with_labels=True, node_size=100, node_color='lightblue', font_size=6, ax=ax)

  # Create a PyQt5 application
  app = QApplication([])
  window = QWidget()
  layout = QVBoxLayout()

  # Create a FigureCanvas object
  canvas = FigureCanvas(fig)
  layout.addWidget(canvas)

  # Set up the window
  window.setLayout(layout)
  window.show()

  # Start the PyQt5 event loop
  app.exec_()




data = []

with open("puzzle_data_as_graph.csv", "r") as f:
    contents = f.readlines()

    for line in contents:
       line = line.strip()
       x, y = line.split(" ")
       data.append((x, y))


visualize_graph_pyqt(data) 



# print(data)



# # Example usage:
# graph_edges = [('A', 'B'), ('B', 'C'), ('A', 'C'), ('C', 'D'), ('D', 'A')]
# visualize_graph(graph_edges) 



