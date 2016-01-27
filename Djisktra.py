__author__ = 'a.jha'

import heapq

MAX = 999999

class Node:
    def __init__(self, v, w):
        self.vertex = v
        self.weight = w

    def __cmp__(self, other):
        return cmp(self.weight, other.weight)


def djikstra(source_node, adjacency_list, min_dist_from_source):
    initial_node = Node(source_node, 0)
    min_dist_from_source[source_node] = 0
    heap = []
    heapq.heappush(heap, initial_node)
    nodes_processed = 0

    try:
        while True:
            node = heapq.heappop(heap)
            nodes_processed += 1
            for alt_node in adjacency_list[node.vertex]:
                alt_weight = min_dist_from_source[node.vertex] + alt_node.weight
                if alt_weight < min_dist_from_source[alt_node.vertex]:
                    min_dist_from_source[alt_node.vertex] = alt_weight
                    alt_node.weight = alt_weight
                heapq.heappush(heap, alt_node)
    except IndexError:
        print('Djikstra ended after processing : {}'.format(nodes_processed))
    finally:
        return min_dist_from_source


if __name__ == '__main__':
    nodes_count = input('Please enter the number of nodes\n')
    adjacency_list = [[] for x in range(nodes_count)]
    min_dist_from_source = [MAX] * nodes_count
    print('Graph will be assumed as directed')
    edges_count = input('Please enter the count of total edges\n')
    print('Please enter the nodes and distance between them for all the edges. '
          'Like 1 2 4, this means edge 1->2 has weight 4')
    for edge in range(edges_count):
        v1, v2, weight = raw_input().split(' ')
        v1 = int(v1) - 1
        v2 = int(v2) - 1
        weight = int(weight)
        adjacency_list[v1].append(Node(v2, weight))
    source_node = input('Please enter the source node')
    source_node -= 1  # Decrementing the index (0-based)
    min_dist_from_source = djikstra(source_node, adjacency_list, min_dist_from_source)
    print('Printing distance matrix :')
    for x in range(nodes_count):
        if x == source_node:
            continue
        print('Distance from source to {} is {}'.format(x, min_dist_from_source[x]))