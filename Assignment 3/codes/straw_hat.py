'''
    This file contains the class definition for the StrawHat class.
'''

from crewmate import CrewMate
from heap import Heap
from treasure import Treasure

class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''
    
    def __init__(self, m):
        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''
        templist=[CrewMate(id=i) for i in range(m)]
        self.crewmates=Heap(lambda x,y:x.load<y.load,templist)
        self.working_crew=[]
        # Write your code here
    def add_treasure(self, treasure):
        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        # assert isinstance(treasure,Treasure)
        crewmate=self.crewmates.top()
        # assert isinstance(crewmate,CrewMate)
        crewmate.add_treasure(treasure)
        if len(crewmate.treasure_list)==1:
            self.working_crew.append(crewmate)
        crewmate.load=max(crewmate.load,treasure.arrival_time)+treasure.size
        self.crewmates.downheap(0)
        # Write your code here
    
    def get_completion_time(self):
        '''
        Arguments:
            None : None
        Returns:
            List[Treasure] : List of treasures in the order of their completion after updating Treasure.completion_time
        Description:
            Returns all the treasure after processing them
        Time Complexity:
            O(n(log(m) + log(n))) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        
        # Write your code here
        answers=[]
        for crewmate in self.working_crew:
            # assert isinstance(crewmate, CrewMate)
            t_initial=[]
            for i in range(len(crewmate.treasure_list)):
                initial_time=crewmate.treasure_list[i].arrival_time
                final_time=0
                if i==(len(crewmate.treasure_list)-1):
                    final_time=float('inf')
                else:
                    final_time=crewmate.treasure_list[i+1].arrival_time
                t_initial.append(crewmate.treasure_list[i].size)
                crewmate.treasures.insert(crewmate.treasure_list[i])
                crewmate.work_on_treasure(initial_time,final_time)
            for i in range(len(crewmate.treasure_list)):
                answers.append(crewmate.treasure_list[i])
                crewmate.treasure_list[i].size=t_initial[i]
        answers.sort(key=lambda treasure: treasure.id)
        return answers
            
    # You can add more methods if required