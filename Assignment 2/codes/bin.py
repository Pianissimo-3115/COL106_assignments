from avl import AVLTree
from node import Node
from object import Object
class Bin:

    def __init__(self, bin_id, capacity):
        self.objects=AVLTree(key=lambda x:x.pointer.id)
        self.capacity=capacity
        self.id=bin_id
    
    def add_object(self, object:Object):
        # Implement logic to add an object to this bin
        self.objects.add(Node(object))
        
    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        self.objects.remove(object_id)
