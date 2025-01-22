from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type=collision_type
        self.element_count=0
        if collision_type == "Chain" or collision_type == "Linear":
            self.table_size=params[1]
            self.list=[None]*self.table_size
            self.parameter=params[0]

        else:
            # Collision type is Double
            # assert collision_type=="Double", "Invalid collision type"  ################################################
            self.table_size=params[3]
            self.list=[None]*self.table_size
            self.parameter1=params[0]
            self.parameter2=params[1]
            self.prime=params[2]



    
    def insert(self, x):

        if isinstance(x, tuple):
            key=x[0]
        else:
            key=x
        temp=self.find(key)
        if temp!=None and temp!=False:
            return
        slot=self.get_slot(key)
        start=slot
        if self.collision_type=="Chain":
            if self.list[slot]==None:
                self.list[slot]=[x]
            else:
                self.list[slot].append(x)

        elif self.collision_type=="Linear":
            while self.list[slot]!=None:
                slot=(slot+1)%self.table_size
                if slot==start:
                    raise Exception("Table is full")
            self.list[slot]=x

        else:
            # assert self.collision_type=="Double", "Invalid collision type"  ################################################
            step=self.prime-self.polynomial_hash(key,self.parameter2,prime=self.prime)%self.prime
            while self.list[slot]!=None:
                slot=(slot+step)%self.table_size
                if slot==start:
                    raise Exception("Table is full")
                
            self.list[slot]=x

        self.element_count+=1
        return slot

    
    def find(self, key):
        
        if self.collision_type=="Chain":
            slot=self.get_slot(key)
            if self.list[slot]==None:
                return None
            for i in self.list[slot]:
                if isinstance(i,str) and i==key:
                    return i
                elif isinstance(i,tuple) and i[0]==key:
                    return i
            return None
        elif self.collision_type=="Linear":
            slot=self.get_slot(key)
            start=slot
            while self.list[slot]!=None:
                if isinstance(self.list[slot], str) and self.list[slot]==key:
                    return self.list[slot]
                elif isinstance(self.list[slot],tuple) and self.list[slot][0]==key:
                    return self.list[slot]
                slot=(slot+1)%self.table_size
                if slot==start:
                    break
            return None
        
        else:
            # assert self.collision_type=="Double", "Invalid collision type"  ################################################
            slot=self.get_slot(key)
            start=slot
            step=(self.prime-self.polynomial_hash(key,self.parameter2,prime=self.prime)%self.prime)
            while self.list[slot]!=None:
                if isinstance(self.list[slot],str) and self.list[slot]==key:
                    return self.list[slot]
                elif isinstance(self.list[slot],tuple) and self.list[slot][0]==key:
                    return self.list[slot]
                slot=(slot+step)%self.table_size
                if slot==start:
                    break
            return None
                    
    
    def mapping(self,letter):
        a=ord(letter)
        if a>=65 and a<=90:
            return a-65+26
        elif a>=97 and a<=122:
            return a-97
        
        else:
            return 0    ########################################################################################
        # else:                                   ############################################################
        #     raise ValueError("Invalid character") ########################################################
        
    def polynomial_hash(self, key, parameter, prime=None, index=0):
        if prime is None:
            prime=self.table_size
        powe=1
        slottt=0
        for i in range(len(key)):
            slottt=(slottt+self.mapping(key[i])*powe)%prime
            powe=(powe*parameter)%prime
        return slottt

        # if prime is None:
        #     prime=self.table_size
        # if index==len(key):
        #     return 0
        # return (self.mapping(key[index])+parameter*self.polynomial_hash(key,parameter,prime,index+1))%prime


    def get_slot(self, key):
        if self.collision_type=="Chain" or self.collision_type=="Linear":
            return self.polynomial_hash(key, self.parameter)
        return self.polynomial_hash(key, self.parameter1)

    
    def get_load(self):
        return self.element_count/self.table_size
    
    def __str__(self):
        if self.collision_type=="Chain":
            newlis=[]
            for i in range(self.table_size):
                if self.list[i]!=None:
                    temp=[]
                    for j in range(len(self.list[i])):
                        if isinstance(self.list[i][j], tuple):
                            temp.append(f"({self.list[i][j][0]}, {self.list[i][j][1]})")
                        else:
                            temp.append(f"{self.list[i][j]}")
                    newlis.append(" ; ".join(temp))
                else:
                    newlis.append("<EMPTY>")
            return " | ".join(newlis)
        else:
            newlis=[]
            for i in range(self.table_size):
                if self.list[i]!=None:
                    if isinstance(self.list[i], tuple):
                        newlis.append(f"({self.list[i][0]}, {self.list[i][1]})")
                    else:
                        newlis.append(f"{self.list[i]}")
                else:
                    newlis.append("<EMPTY>")
            return " | ".join(newlis)
    
    def rehash(self):
        newsize=get_next_size()
        oldlist=[]
        if self.collision_type=="Chain":
            oldlist=[l[:] for l in self.list if l is not None]
        else:
            oldlist=self.list[:]
        self.table_size=newsize
        self.list=[None]*newsize
        self.element_count=0
        if self.collision_type=="Chain":
            for i in oldlist:
                for j in i:
                    if i is not None:
                        self.insert(j)
        else:
            for i in oldlist:
                if i is not None:
                    self.insert(i)
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def find(self, key):
        outp=super().find(key)
        if outp==None:
            return False
        return True
    
class HashMap(HashTable):    
    def find(self, key):
        outp=super().find(key)
        if outp==None:
            return None
        return outp[1]