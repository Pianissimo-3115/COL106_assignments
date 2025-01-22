from node import *

class AVLTree:

    def __init__(self,key): 
        self.root = None
        self.key=key
    
    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def add(self,node):
        self.root=self.insert(self.root,node)
    
    def insert(self, root=None, node=None):
        assert isinstance(node,Node)
        if not root:
            return node
        assert isinstance(root,Node)
        if self.key(node) < self.key(root):
            root.left = self.insert(root.left,node)
        else:
            root.right = self.insert(root.right, node)
        
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left rotation
        if balance > 1 and self.key(node)<self.key(root.left):
            return self.right_rotate(root)
        
        # Right rotation
        if balance < -1 and  self.key(node)>self.key(root.right):
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.key(node)>self.key(root.left):
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.key(node)<self.key(root.right):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root:None, value):
        if not root:
            return root
        assert isinstance(root,Node)

        if value < self.key(root):
            root.left = self.delete(root.left, value)
        elif value > self.key(root):
            root.right = self.delete(root.right, value)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            temp = self.min_value_node(root.right)
            assert isinstance(temp,Node)
            root.pointer=temp.pointer
            root.right = self.delete(root.right, self.key(temp))

        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def min_value_node(self, root:Node):
        current = root
        while current.left:
            current = current.left
        return current
    
    def max_value_node(self,root:Node):
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
    
    def searchcap(self,root:Node,node:Node):
        if not root or self.key(root)[0]==self.key(node)[0]:
            return root
        if self.key(root)[0]<self.key(node)[0]:
            return self.search(root.right,node)
        return self.search(root.left,node)
    
    def bluefind(self):
        return self.min_value_node(self.root)
    
    def greenfind(self):
        return self.max_value_node(self.root)
    
    def yellowfind(self):
        temp=self.searchcap(self.min_value_node(self.root))
        while temp.right and self.key(temp.right)[0]==self.key(temp)[0]:
            temp=temp.right
        return temp
    
    def redfind(self):
        temp=self.searchcap(self.max_value_node(self.root))
        while temp.left and self.key(temp.left)[0]==self.key(temp)[0]:
            temp=temp.left
        return temp
        