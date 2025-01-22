from node import *
import pdb
class AVLTree:
    def __init__(self,key): 
        self.root = None
        def keynew(node:Node):
            if node:
                return key(node)
            else:
                return None
        self.key=keynew    
    def height(self, node):
        if not node:
            return 0
        return node.height

    def _diff(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def add(self,node):
        assert isinstance(node,Node),"node is not Node"
        self.root=self._insert(self.root,node)
    
    def _insert(self, root, node):
        if not root:
            return node
        assert isinstance(root,Node),"root is not Node"
        if self.key(node) < self.key(root):
            root.left = self._insert(root.left,node)
        else:
            root.right = self._insert(root.right, node)
        
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        bal = self._diff(root)
        if bal>1:
            if self.key(node)<self.key(root.left):
                return self._right_rotate(root)
            else:
                root.left=self._left_rotate(root.left)
                return self._right_rotate(root)
        if bal<-1:
            if self.key(node)>self.key(root.right):
                return self._left_rotate(root)
            else:
                root.right=self._right_rotate(root.right)
                return self._left_rotate(root)
        return root
   
    def remove(self,value):
        self.root=self._delete(self.root,value)
    
    def _delete(self, root, value):
        if not root:
            return root
        assert isinstance(root,Node),"root is not Node"

        if value < self.key(root):
            root.left = self._delete(root.left, value)
        elif value > self.key(root):
            root.right = self._delete(root.right, value)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            temp = self._min_value_node(root.right)
            assert isinstance(temp,Node),"temp is not Node"
            root.pointer=temp.pointer
            root.right = self._delete(root.right, self.key(temp))

        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        bal = self._diff(root)

        if bal>1:
            if self._diff(root.left)>=0:
                return self._right_rotate(root)
            else:
                root.left=self._left_rotate(root.left)
                return self._right_rotate(root)
        if bal<-1:
            if self._diff(root.right)<=0:
                return self._left_rotate(root)
            else:
                root.right=self._right_rotate(root.right)
                return self._left_rotate(root)
        return root

    def _left_rotate(self, z):
        nextnode = z.right
        nextnext = nextnode.left

        nextnode.left = z
        z.right = nextnext

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        nextnode.height = 1 + max(self.height(nextnode.left), self.height(nextnode.right))

        return nextnode

    def _right_rotate(self, z):
        nextnode = z.left
        nextnext = nextnode.right

        nextnode.right = z
        z.left = nextnext

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        nextnode.height = 1 + max(self.height(nextnode.left), self.height(nextnode.right))

        return nextnode

    def _min_value_node(self, root):
        if not root:
            return None
        current = root
        while current.left:
            current = current.left
        return current
    
    def _max_value_node(self,root):
        if not root:
            return None
        current=root
        while current.right:
            current=current.right
        return current
    
    def search(self, root, value):
        if not root or self.key(root) == value:
            return root
        if self.key(root) < value:
            return self.search(root.right, value)
        return self.search(root.left, value)
    
    def _searchcap(self,root,node):
        if not node:
            return None
        if not root or self.key(root)[0]==self.key(node)[0]:
            return root
        
        assert isinstance(root,Node)
        assert isinstance(node,Node)
        if self.key(root)[0]<self.key(node)[0]:
            return self._searchcap(root.right,node)
        return self._searchcap(root.left,node)
    
    def _find_min_range(self,root,size):
        if not root:
            return None
        if self.key(root)[0]<size:
            return self._find_min_range(root.right,size)
        if self.key(root)[0]>=size:
            temp=self._find_min_range(root.left,size)
            if temp:
                return temp
            return root
    
    def _find_max_id(self,root,capacity):
        if not root:
            return None
        if self.key(root)[0]==capacity:
            temp=self._find_max_id(root.right,capacity)
            if temp: return temp
            return root
        return self._find_max_id(root.left,capacity)
        
    def _find_min_id(self,root,capacity):
        if not root:
            return None
        if self.key(root)[0]==capacity:
            temp=self._find_min_id(root.left,capacity)
            if temp: return temp
            return root
        return self._find_min_id(root.right,capacity)

    def bluefind(self,size):
        return self._find_min_range(self.root,size)
    
    def greenfind(self,size):
        temp=self._max_value_node(self.root)
        if not temp:
            return None
        if self.key(temp)[0]>=size:
            return temp
        else: return None
    
    def yellowfind(self,size):
        node=self._find_min_range(self.root,size)
        temp=self._searchcap(self.root,node)
        if not temp:
            return None
        new=self._find_max_id(temp,self.key(temp)[0])
        return new
    
    def redfind(self,size):  
        temp=self._searchcap(self.root,self._max_value_node(self.root))
        if not temp:
            return None
        if self.key(temp)[0]<size:
            return None
        new=self._find_min_id(temp,self.key(temp)[0])
        return new
        
    def inorder(self):
        result = []
        def traverse(node):
            if node is not None:
                traverse(node.left)
                result.append(self.key(node))
                traverse(node.right)
            return
        traverse(self.root)
        return result