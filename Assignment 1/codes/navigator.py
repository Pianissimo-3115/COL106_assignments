from maze import *
from exception import *
from stack import *
# import pdb

class PacMan:
    def __init__(self, grid : Maze) -> None:
        ## DO NOT MODIFY THIS FUNCTION
        self.navigator_maze = grid.grid_representation
    def find_path(self, start : tuple[int, int], end : tuple[int, int]) -> list[tuple[int, int]]:
        self.stack=Stack()

        # IMPLEMENT FUNCTION HERE
        def adj(point):
            ret=[]
            if point[0]!=0: ret.append([point[0]-1,point[1]])
            if point[0]!=len(self.navigator_maze)-1: ret.append([point[0]+1,point[1]])
            if point[1]!=0: ret.append([point[0],point[1]-1])
            if point[1]!=len(self.navigator_maze[0])-1: ret.append([point[0],point[1]+1])
            return ret
        visited=[]
        for i in range(len(self.navigator_maze)):
            temp=[]
            for j in range(len(self.navigator_maze[0])):
                temp.append(False)
            visited.append(temp)
        self.stack.push(start)
        poss=True
        while True:
            a=self.stack.top
            if(a is None):
                poss=False
                break 
            """
            if(visited[a[0]][a[1]]): 
                poss=False
                break
            """
            visited[a[0]][a[1]]=True
            if(a==(end[0],end[1])): 
                break
            adjj=adj(a)
            # print(self.stack.list,"firstagain")
            for i in adjj:
                if(not visited[i[0]][i[1]]):
                    if(self.navigator_maze[i[0]][i[1]]!=1):
                        self.stack.push(tuple(i))
                        break
            else:
                x=self.stack.pop()
        if(poss): return self.stack.list
        else: raise PathNotFoundException

