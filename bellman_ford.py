from math import log


def negative_logarithm_convertor(graph):
    """ Takes the log of each rate in graph and negate it"""
    result = [[-log(edge) for edge in row] for row in graph]
    return result


def arbitrage(currencies, rates_matrix):
    """ Calculates arbitrage situations and prints out the details of this calculation"""
    trans_graph = negative_logarithm_convertor(rates_matrix)
    source = 0
    n = len(trans_graph)
    min_dist = [float('inf')] * n

    pre = [-1] * n

    min_dist[source] = source

    # 'Relax edges |V-1| times'
    for _ in range(n - 1):
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                    pre[dest_curr] = source_curr

    # if we can still relax edges, then we have a negative cycle
    for source_curr in range(n):
        for dest_curr in range(n):
            if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                # negative cycle exists, and use the predecessor chain to print the cycle
                print_cycle = [dest_curr, source_curr]
                # Start from the source and go backwards until you see the source vertex again or any vertex that
                # already exists in print_cycle array
                while pre[source_curr] not in print_cycle:
                    print_cycle.append(pre[source_curr])
                    source_curr = pre[source_curr]
                print_cycle.append(pre[source_curr])
                print("\nARBITRAGE:")
                print(" --> ".join([currencies[p] for p in print_cycle[::-1]]))
