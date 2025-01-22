from bin import Bin
from avl import AVLTree
from object import Object, Color
from node import Node
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self): 
        # Maintain all the Bins and Objects in GCMS
        self.bins1=AVLTree(lambda node: (node.pointer.capacity,node.pointer.id))
        self.bins2=AVLTree(lambda node: node.pointer.id)
        self.objects=AVLTree(lambda node: node.pointer.id)

    def add_bin(self, bin_id, capacity):
        newbin=Bin(bin_id,capacity)
        self.bins1.add(Node(newbin))
        self.bins2.add(Node(newbin))

    def add_object(self, object_id, size, color):
        newobj=Object(object_id,size,color)
        bin=None
        if newobj.color==Color.BLUE:
            bin=self.bins1.bluefind(size)
        elif newobj.color==Color.YELLOW:
            bin=self.bins1.yellowfind(size)
        elif newobj.color==Color.RED:
            bin=self.bins1.redfind(size)
        else:
            bin=self.bins1.greenfind(size)
        if not bin:
            raise NoBinFoundException
        self.objects.add(Node(newobj))
        binnew=bin.pointer
        assert isinstance(binnew,Bin),"bin is not Bin"
        self.bins1.remove((binnew.capacity,binnew.id))
        binnew.add_object(newobj)
        binnew.capacity-=size
        newobj.bin=binnew
        self.bins1.add(Node(binnew))
   
    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin

        obj1=self.objects.search(self.objects.root,object_id)
        if not obj1:
            return
        obj=obj1.pointer
        assert isinstance(obj,Object),"obj is not Object"
        thisbin=obj.bin
        if not thisbin:
            return
        assert isinstance(thisbin,Bin)
        self.objects.remove(object_id)
        self.bins1.remove((thisbin.capacity,thisbin.id))
        thisbin.remove_object(object_id)
        thisbin.capacity+=obj.size
        obj.bin=None
        self.bins1.add(Node(thisbin))

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        curbin=self.bins2.search(self.bins2.root,bin_id).pointer
        assert isinstance(curbin,Bin)
        newlist=curbin.objects.inorder()
        return (curbin.capacity,newlist)

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        obj1=self.objects.search(self.objects.root,object_id)
        if not obj1:
            return None
        obj=obj1.pointer
        assert isinstance(obj,Object)
        if not obj.bin:
            return None
        return obj.bin.id
    
    