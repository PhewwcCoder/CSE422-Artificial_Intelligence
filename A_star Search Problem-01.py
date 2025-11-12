# =========================================================
# Assignment 01 – A* Search Algorithm (CSE422)
# Question PDF: https://github.com/PhewwcCoder/CSE422-Artificial_Intelligence/blob/main/Docs/Assignement01_(A-%20Search)%20-%20Copy.pdf
# =========================================================

import sys, heapq
input = sys.stdin.readline

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

def main():
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
        visited[row][col] == True

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

if __name__ == "__main__":
    main()
    