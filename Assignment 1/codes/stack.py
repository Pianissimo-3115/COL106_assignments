class Stack:
    def __init__(self) -> None:
        #YOU CAN (AND SHOULD!) MODIFY THIS FUNCTION
        self.list=[]
        self.top=None
    def push(self,a):
        self.list.append(a)
        self.top=a
        pass
    def pop(self):
        temp=self.list.pop()
        if len(self.list)==0:
            self.top=None
        else: self.top=self.list[-1]
        return temp
    # You can implement this class however you like