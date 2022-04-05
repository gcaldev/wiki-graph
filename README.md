# Wiki Graph
## Introduction
This project was developed in group composed by a university teammate and me. The project objetive was to parse a portion of Wikipedia and be able to operate with that data through graphs. We implemented the graph structure with particular methods to do certain operations that will be explained below. Also to make this posible we implemented a Stack and a Queue.

## Execution
If you want to run this terminal app you should run netstats.py

## Graph representation.
Each graph represented an individual Wikipedia page and each hyperlink that pointed to other topics were represented as the relation between graphs. The graph's type was directed and implemented as a dictionary of dictonaries.

## Features

### Shortest Path problem
We implemented a method to find the shortest path between two nodes of the graph in linear time complexity.
- Command : camino.

### Connected set of nodes
This method allows you to find all the nodes that are in the same graph component with the received node.
- Command : conectados.

### Posible way to read pages
This method returns a posible way to read a set of pages received.
- Command : lectura.

### Diameter of the graph
This functionality allows you to find the diameter, to find it the program will return the greatest of the shortest paths in the graph.
- Command : diametro

### Range N 
We implemented this to be able to find all pages that are at a distance of N from the received page(In term of links redirections).
- Command : rango

### Community Detection
This basic algorithm allows you to detect the community in which the received graph is part. A community is composed by the nodes that are highly related.
- Command : comunidad

### First Page Navigation
This will return a list with the 20 first pages that we would find if we click on the first hyperlink that appears.
- Command : navegacion

### Find cycle
This program will find a cycle in the graph
- Command : ciclo