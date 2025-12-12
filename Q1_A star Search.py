# =========================================================
# Question PDF: https://github.com/PhewwcCoder/CSE422-Artificial_Intelligence/blob/main/Docs/Q1_(A%20star%20Search).pdf
# =========================================================

import sys, heapq   #heapq always pops the smallest priority item, which is exactly what A* needed.
from collections import deque
input = sys.stdin.readline

#PART-01
def manhattan_distance(r1, c1, r2, c2):
    return abs(r1-r2)+abs(c1-c2)

def in_bounds(r, c, n, m):
    return 0 <= r <n and 0 <= c <m

#Reconstruct Path from Parents
#sr --> start row, gc --> goal column
def reconstruct_path(parent, sr, sc, gr, gc):
    moves = []
    row, col = gr, gc
    while not (row == sr and col == sc):
        parent_row, parent_col, move = parent[row][col]
        moves.append(move)
        row, col = parent_row, parent_col
    moves.reverse()
    return "".join(moves)

def PART1():
    n,m = map(int, input().split())
    a,b = map(int, input().split())
    c,d = map(int, input().split())

    grid = []   #Taking maze description
    for i in range(n):
        grid.append(input().strip())    #strip() removes all extra whitespaces from both the beginning and the end of the input string

    if not in_bounds(a,b,n,m) or not in_bounds(c,d,n,m):
        print(-1); return
    if grid[a][b] == "#" or grid[c][d] == "#":
        print(-1); return
    if a == c and b == d:
        print(0); return 
    
    INF = 10**18
    g_cost = [[INF]*m for _ in range(n)]
    parent = [[None]*m for _ in range(n)]
    visited = [[False]*m for _ in range(n)]

    direction_row = [-1,1,0,0]
    direction_col = [0,0,-1,1]
    moves = ['U','D','L','R']

    g_cost[a][b] = 0
    h0 = manhattan_distance(a,b,c,d)
    pq = []
    heapq.heappush(pq, (h0, 0, a, b))
    tie_breaker = 0

    while pq:
        f, tb, row, col = heapq.heappop(pq)
        if visited[row][col]:
            continue
        visited[row][col] = True

        if row == c and col == d:
            path = reconstruct_path(parent,a,b,c,d)
            print(len(path))
            print(path)
            return
        
        for i in range(4):
            child_row = row + direction_row[i]
            child_col = col + direction_col[i]
            if not in_bounds(child_row,child_col,n,m):
                continue
            if grid[child_row][child_col] == "#":
                continue

            new_g = g_cost[row][col] + 1
            if new_g < g_cost[child_row][child_col]:
                g_cost[child_row][child_col] = new_g
                parent[child_row][child_col] = (row, col, moves[i]) 
                heuristic = manhattan_distance(child_row,child_col,c,d)
                f2 = new_g + heuristic
                tie_breaker += 1
                heapq.heappush(pq, (f2, tie_breaker, child_row, child_col))       
    print(-1)


def PART2():
    n,m = map(int, input().split()) #n=number of vertices, m=number of edges
    a,b = map(int, input().split())
    heuristic_list = [0]*(n+1)
    for i in range(n):
        x,y = map(int, input().split())
        heuristic_list[x] = y

    #Building adjacency list for undirected graph
    adj_list = [[] for _ in range(n+1)]
    for j in range(m):
        u,v = map(int, input().split())
        adj_list[u].append(v)
        adj_list[v].append(u)

    #BFS from goal node to compute true distances dist[v] to goal
    INF = 10**18
    dist = [INF]*(n+1)

    dist[b] = 0
    dq = deque()    #Queue object created
    dq.append(b)    #source node added(for this context--> goal node)

    while dq:
        u = dq.popleft()    #deque
        for v in adj_list[u]:   #check the neighbors
            if dist[v] == INF:  #If not visited then visit the node
                dist[v] = dist[u]+1
                dq.append(v)

    #Checking admissibility
    bad_nodes = []  #Storing nodes which arent admissible
    for v in range(1,n+1):
        if dist[v] == INF:
            continue
        if heuristic_list[v] > dist[v]:
            bad_nodes.append(v)

    if not bad_nodes:
        print(1)
    else:
        print(0)
        print('Here nodes', *bad_nodes, 'are not admissible')

if __name__ == "__main__":
    PART1()
    PART2()

    
'''    
Example Sample-01(for PART-2)
5 5
2 4
1 0
2 2
3 2
4 0
5 1
5 2
2 3
1 4
4 5
5 3

Example Sample-02
6 7
1 6
1 6
2 4
3 2
4 5
5 2
6 0
1 2
2 3
3 6
1 4
4 5
5 6
3 5
'''