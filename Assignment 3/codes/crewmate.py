'''
    Python file to implement the class CrewMate
'''
from heap import Heap
from treasure import Treasure
class CrewMate:
    '''
    Class to implement a crewmate
    '''
    
    def __init__(self):
        '''
            Initializes the crewmate
        '''
        self.treasures=Heap(comparison_function=lambda x,y:(((x.arrival_time+x.size),x.id)<((y.arrival_time+y.size),y.id)))
        self.load=0
        self.treasure_list=[]
        # Write your code here
    def add_treasure(self,treasure:Treasure):
        '''
        Arguments:
            treasure :Treasure: Treasure to be added to this crewmate
        Returns:
            None
        Description:
            Add the treasure to be processed by this crewmate
        '''
        # self.treasures.insert(treasure)
        self.treasure_list.append(treasure)
    
    def work_on_treasure(self,initial_time,final_time): #Initial time is current time, and final time is "itne time tk kaam karo"
        time=initial_time
        while time<final_time:
            treasure=self.treasures.top()
            if not treasure:
                return
            # assert isinstance(treasure,Treasure)
            if treasure.size<(final_time-time):
                time+=treasure.size
                treasure.completion_time=time
                self.treasures.extract()
            else:
                treasure.size-=(final_time-time)
                time=final_time
    # Add more methods if required
