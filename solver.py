# A* solver
from heapq import *
from functools import total_ordering
from typing import Callable, List
from copy import deepcopy

from PIL.Image import TRANSPOSE

PATH_COST = 1

class Heap():
    def __init__(self):
        self.arr = []
        
    def size(self):
        return len(self.arr)
    
    def clear(self):
        self.arr.clear()
        
    def isEmpty(self):
        return len(self.arr) == 0
    
    def push(self, cost, element):
        heappush(self.arr, (cost, element))
        pass
    
    def pop(self):
        res = heappop(self.arr)
        return res[1]
    
    def printHeap(self):
        print(self.arr)
        
@total_ordering
class Node():
    def __init__(self, state : list):
        self.state = state
        self.visited = False
        self.isInFrontier = False
        self.bestCost = 10**8
        self.isExpanded = False
        
    def __lt__(self, other):
        # lexicographical order
        return str(self.getStateLabel())< str(other.getStateLabel())
        
    def getState(self) -> list:
        return self.state
    
    def getStateLabel(self):
        res = ""
        for pos in self.state:
            if pos >= 0:
                res+=str(pos)
            else:
                res += "x"
        return res

class AStarSolver():
    def __init__(self, state : list, action : Callable, heuristic : Callable):
        self.init : Node = Node(state)
        self.action : Callable = action
        self.frontier = Heap()
        self.heuristic : Callable = heuristic
        self.stateDict = {}
        self.path = []
      
    def solve(self):
        self.path = []
        self.init.bestCost = 0
        self.frontier.push(0, self.init)
        # this 
        if self.heuristic(self.init.getState()):
            print("Initial state is already invalid, how can we solve it?")
            return self
        while not self.frontier.isEmpty():
            node : Node = self.frontier.pop()
            node.isInFrontier = True
            self.path.append(node.getState())
            
            # Test if popped node is goal
            if self.goalTest(node):
                print("Final result: ", node.getState())
                return self
            
            # Add node to expanded
            node.isExpanded = True
            for adjNode in self.generateNextNodes(node):
                if adjNode.isInFrontier:
                    # Update path cost
                    newCost = self.calculateCost(node, adjNode)
                    if(adjNode.bestCost > newCost):
                        adjNode.bestCost = newCost
                    continue
                elif (not adjNode.isInFrontier) and (not adjNode.isExpanded):
                    # Calculate new cost
                    newCost = self.calculateCost(node, adjNode)
                    adjNode.bestCost = newCost
                    # New node to the frontier
                    self.frontier.push(newCost, adjNode)
                    
        # If it go out of the loop, probably it fail
        print("Fail to find the result!!")
        return self
    
    def goalTest(self, node : Node) -> bool:
        state = node.getState()
        if self.heuristic(state) != 0:
            return False
        # Improvement: Check backward
        for i in range(len(state)-1, -1, -1):
            if(state[i] == -1): return False
        return True
    
    
    def calculateCost(self, parent, node):
        return parent.bestCost + PATH_COST + self.heuristic(node.getState())
    
    def generateNextNodes(self, node : Node) -> List[Node]:
        states = self.action(node.getState())
        result = []
        for newState in states:
            newNode = Node(newState)
            label = newNode.getStateLabel()
            if not label in self.stateDict:
                self.stateDict[label] = newNode
            result.append(self.stateDict[label])
        return result
    
    def getResult(self, isPrint : bool):
        if(len(self.path) == 0):
            print("Run the solve() function first!!")
            return []
        if isPrint:
            print("This is the path:")
            print(self.path)
        return self.path

def action(state : list) -> list:
    if(len(state) != 8):
        return []
    # Just make 8 state of that row
    for pos in range(len(state)):
        if (state[pos] == -1):
            newStates = []
            for i in range(8):
                tmp = deepcopy(state)
                tmp[pos] = i
                newStates.append(tmp)
            return newStates
    return []

def num_attacking_pairs (status: List[int]) -> int:
  res = 0
  for i in range(8):
    if status[i] == -1:
      continue
    for j in range(i + 1, 8):
      if status[j] == -1:
        continue
      if status[i] == status[j] or i + status[i] == j + status[j] or i - status[i] == j - status[j]:
        res += 1

  return res

def heuristic(state) -> int:
    return num_attacking_pairs(state)
            
intiState = [6, -1, -1, -1, -1, -1, -1, -1]
solver  = AStarSolver(intiState, action, heuristic)
solver.solve()
res = solver.getResult(isPrint=True)
print("Count:", len(res))