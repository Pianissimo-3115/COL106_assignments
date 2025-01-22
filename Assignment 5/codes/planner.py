from flight import Flight,City


class Queue:
    def __init__(self, size):
        self.front = 0
        self.rear = -1
        self.size = size
        self.queue = [None] * size
        self.count = 0

    def enqueue(self, data):
        if self.size==self.count:
            return
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = data
        self.count+=1

    def dequeue(self):
        if self.count ==0:
            return
        data = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.size
        self.count-=1
        return data
        
    def is_empty(self):
        return self.count==0
class Heap:
    def __init__(self,init_array, comparison_function=lambda x,y: x<y):
        self.comparison_function=comparison_function    #If x is at top of the heap, comparison_function(x,y)=True for all y in heap except x itself
        n=len(init_array)
        self.array:list=init_array
        for i in range(n-1,-1,-1):
            self.downheap(i)
        self.last=n-1
        
    def insert(self, value):
        self.array.append(value)
        self.last+=1
        self._upheap(self.last)
    
    def extract(self):
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
        if len(self.array)==0: return None
        return self.array[0]
    
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

class Planner:
    def __init__(self, flights : list[Flight]):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = flights
        self.flight_count=len(flights)+1
        self.cities:list[City]=[]
        self.city_count=0
        for flight in flights:
            self.city_count=max(self.city_count,flight.start_city,flight.end_city)
        self.city_count+=1
        for i in range(self.city_count):
            self.cities.append(City(i))
        for flight in flights:
            flight.dep_city=self.cities[flight.start_city]
            flight.arr_city=self.cities[flight.end_city]
            flight.dep_city.departing_flights.append(flight)
            flight.arr_city.arriving_flights.append(flight)



    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """ from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if start_city==end_city:
            return []
        nq=Queue(self.flight_count)
        final_dist=None
        final_ans=(float('inf'),float('inf'))
        final_flight=None
        for flight in self.cities[start_city].departing_flights:
            # assert isinstance(flight,Flight)    ##########################################################################
            if flight.departure_time<t1 or flight.arrival_time>t2:
                continue
            visited=[False for i in range(self.flight_count+1)]
            nq.enqueue((flight,1))      # flight, depth
            
            breakin=float('inf')
            best_ans=(float('inf'),float('inf'))
            best_flight=None
            dist=[None for i in range(self.flight_count+1)] # to store previous flights
            while not nq.is_empty():
                cur_flight,cur_depth=nq.dequeue()
                if cur_depth>breakin:
                    break
                if not visited[cur_flight.flight_no] and cur_flight.departure_time>=t1 and cur_flight.arrival_time<=t2:
                    visited[cur_flight.flight_no]=True
                if cur_flight.end_city==end_city:
                    if (cur_depth,cur_flight.arrival_time)<best_ans:
                        best_ans=(cur_depth,cur_flight.arrival_time)
                        best_flight=cur_flight
                        breakin=cur_depth
                else:
                    for newflight in cur_flight.arr_city.departing_flights:
                        if not visited[newflight.flight_no] and newflight.departure_time>=cur_flight.arrival_time+20 and newflight.arrival_time<=t2:
                            nq.enqueue((newflight,cur_depth+1))
                            dist[newflight.flight_no]=cur_flight
                            visited[newflight.flight_no]=True

            if best_ans<final_ans:
                final_ans=best_ans
                final_dist=dist[:]
                final_flight=best_flight

        if final_flight is None:
            return []
        route=[]
        # assert isinstance(final_flight,Flight)        ###########################################################################################
        while final_flight is not None:
            route.append(final_flight)
            final_flight=final_dist[final_flight.flight_no]
        return route[::-1]

    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        if start_city == end_city: return []
        dist=[(float('inf'),None) for i in range(self.flight_count+1)]   # (accumulated_cost,prev_flight)

        mh=Heap(init_array=[])        
        mh.insert((0,start_city,None))   # (city,flight)
        visited=[False for i in range(self.flight_count+1)]
        while mh.top()!=None:
            cur_cost,cur_city,best_flight=mh.extract()

            if cur_city==end_city:
                continue
            if best_flight is not None:
                if visited[best_flight.flight_no]:
                    continue
                visited[best_flight.flight_no]=True
            for flight in self.cities[cur_city].departing_flights:
                temp=None
                temp2=None
                if best_flight is not None:
                    temp=best_flight.arrival_time
                    temp2=dist[best_flight.flight_no][0]
                else:
                    temp=t1-20
                    temp2=0
                if flight.departure_time>=temp+20 and flight.arrival_time<=t2:
                    if dist[flight.flight_no][0]>temp2+flight.fare:
                        dist[flight.flight_no]=(temp2+flight.fare,best_flight)
                        mh.insert((temp2+flight.fare,flight.end_city,flight))
        if dist[end_city]==float('inf'):
            return []
        route=[]
        cur_city=end_city
        best_final_flight=None
        best_cost=float('inf')
        for flight in self.cities[end_city].arriving_flights:
            if flight.arrival_time<=t2 and flight.departure_time>=t1:
                if dist[flight.flight_no][0]<best_cost:
                    best_cost=dist[flight.flight_no][0]
                    best_final_flight=flight

        while best_final_flight is not None:
            route.append(best_final_flight)
            best_final_flight=dist[best_final_flight.flight_no][1]
            
        return route[::-1]

        
        
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        if start_city == end_city: return []
        dist=[((float('inf'),float('inf')),None) for i in range(self.flight_count+1)]   # ((no of flights,accumulated_cost),prev_flight)
        # for flight in self.cities[start_city].departing_flights:
        #     dist[flight.flight_no]=((1,flight.fare),None)
        mh=Heap(init_array=[])        
        mh.insert((0,start_city,None))   # (city,flight)
        visited=[False for i in range(self.flight_count+1)]
        while mh.top()!=None:
            cur_cost,cur_city,best_flight=mh.extract()
            if cur_city==end_city:
                continue
            if best_flight is not None:
                if visited[best_flight.flight_no]:
                    continue
                visited[best_flight.flight_no]=True
            for flight in self.cities[cur_city].departing_flights:
                temp=None
                temp2=None
                if best_flight is not None:
                    temp=best_flight.arrival_time
                    temp2=dist[best_flight.flight_no][0]
                else:
                    temp=t1-20
                    temp2=(0,0)
                if flight.departure_time>=temp+20 and flight.arrival_time<=t2:
                    if dist[flight.flight_no][0]>(temp2[0]+1,temp2[1]+flight.fare):
                        dist[flight.flight_no]=((temp2[0]+1,temp2[1]+flight.fare),best_flight)
                        mh.insert(((temp2[0]+1,temp2[1]+flight.fare),flight.end_city,flight))

        if dist[end_city]==float('inf'):
            return []
        route=[]
        cur_city=end_city
        best_final_flight=None
        best_cost=(float('inf'),float('inf'))
        for flight in self.cities[end_city].arriving_flights:
            if flight.arrival_time<=t2 and flight.departure_time>=t1:
                if dist[flight.flight_no][0]<best_cost:
                    best_cost=dist[flight.flight_no][0]
                    best_final_flight=flight

        while best_final_flight is not None:
            route.append(best_final_flight)
            best_final_flight=dist[best_final_flight.flight_no][1]
            
        return route[::-1]