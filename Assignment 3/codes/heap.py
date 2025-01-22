'''
Python Code to implement a heap with general comparison function
'''
class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array=[]):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        self.comparison_function=comparison_function    #If x is at top of the heap, comparison_function(x,y)=True for all y in heap except x itself
        n=len(init_array)
        self.array=init_array
        for i in range(n-1,-1,-1):
            self.downheap(i)
        self.last=n-1
        # Write your code here
        
    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        self.array.append(value)
        self.last+=1
        self._upheap(self.last)
        # Write your code here
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        if len(self.array)==0:
            return None
        temp=self.array[0]
        if self.last==0:
            self.array.pop()
            self.last-=1
            return temp
        self.array[0]=self.array[self.last]
        self.array.pop()
        self.last-=1
        self.downheap(0)
        return temp
    
    def top(self):
        '''
        Arguments:
            None : None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        if len(self.array)==0: return None
        return self.array[0]
    
    # You can add more functions if you want to
    def downheap(self,index):
        a=index
        while 2*a+1<len(self.array):
            minind=2*a+1
            if 2*a+2<len(self.array) and self.comparison_function(self.array[2*a+2],self.array[2*a+1]):
                minind=2*a+2
            if not self.comparison_function(self.array[minind],self.array[a]):
                break
            self.array[minind],self.array[a]=self.array[a],self.array[minind]
            a=minind
    
    def _upheap(self,index):
        a=index
        while a>0:
            parent=(a-1)//2
            if self.comparison_function(self.array[a],self.array[parent]):
                self.array[parent],self.array[a]=self.array[a],self.array[parent]
                a=parent
            else:
                break

