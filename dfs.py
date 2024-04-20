from typing import List
from collections import deque
import pygame

visited = set()
dq = deque()
parent = dict()

#initialState = 'red,blue blue,red empty empty'
#N = 2

initialState = 'red,blue,green green,blue,red green,blue,red empty empty'
N = 3

def print_steps(bottles: List[List[str]]):
    b = wrap(bottles)
    while b != initialState:
        print(b)
        b = parent[b]
    print(initialState)

def unwrap(state: str):
    entries = state.split(' ')
    bottles = [e.split(',') if e != 'empty' else [] for e in entries]
    return bottles

def wrap(bottles: List[List[str]]):
    return ' '.join([','.join(e) if e else 'empty' for e in bottles])

def check(bottles: List[List[str]]):
    c = lambda b: b == [] or (len(b) == N and all(x == b[0] for x in b))
    return all(map(c, bottles))

def can_pour(b1: List[str], b2: List[str]):
    if not b1:
        return 0
    
    count = 0
    for c in reversed(b1):
        if b2 and c != b2[-1]:
            break
        if not b2 and c != b1[-1]:
            break
        count += 1
    
    return min(count, N - len(b2))

def bfs(initialState: str):
    dq.append(initialState)
    
    while dq:
        bottles = unwrap(dq[0])
        
        if check(bottles):
            print_steps(bottles)
            return
        
        visited.add(dq[0])
        dq.popleft()
        
        i : int = 0
        while i < len(bottles):
            j : int = 0
            while j < len(bottles):
                
                n = can_pour(bottles[i], bottles[j])
                
                if n > 0:
                    bottles_cpy = bottles.copy()
                    bottles[j] = bottles[j] + bottles[i][len(bottles[i]) - n:]
                    bottles[i] = bottles[i][0:len(bottles[i]) - n]
                    
                    wb = wrap(bottles)
                    
                    if wb not in visited:
                        parent[wb] = wrap(bottles_cpy)
                        dq.append(wb)
                    
                    bottles = bottles_cpy
                j += 1
            i += 1
    print("No solution exists!")

bfs(initialState)
