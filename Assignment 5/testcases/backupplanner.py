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
        answer=[None for i in range(self.flight_count+1)]
        # mere queue mei ek tuple hoga (flight,prev_flight,depth)
        visited=[False for i in range(self.flight_count)]
        for flight in self.cities[start_city].departing_flights:
            if flight.departure_time>=t1 and flight.arrival_time<=t2:
                nq.enqueue((flight,None,1))

        while not nq.is_empty():
            temp1=None
            flight,prev_flight,depth=nq.dequeue()
            visited[flight.flight_no]=True
            if prev_flight is not None:
                temp1=prev_flight.arrival_time
            else:
                temp1=t1-20
            if flight.arr_city.city_no==end_city:
                break
            for next_flight in self.cities[flight.end_city].departing_flights:
                if next_flight.departure_time>=temp1+20 and next_flight.arrival_time<=t2 and not visited[next_flight.flight_no]:
                    nq.enqueue((next_flight,flight,depth+1))
                    answer[next_flight.flight_no]=(flight,depth)
                    visited[next_flight.flight_no]=True
            
        returning=False
        for flight in self.cities[end_city].arriving_flights:
            if flight.arrival_time<=t2 and flight.departure_time>=t1 and visited[flight.flight_no]:
                returning=True
                break
        if not returning:
            return []
        route=[]
        cur_flight=None
        cur_time=float('inf')
        for flight in self.cities[end_city].arriving_flights:
            if flight.arrival_time<=t2 and flight.departure_time>=t1 and visited[flight.flight_no]:
                if cur_time>flight.arrival_time:
                    cur_time=flight.arrival_time
                    cur_flight=flight
        route.append(cur_flight)
        while answer[cur_flight.flight_no] is not None:
            route.append(answer[cur_flight.flight_no][0])
            cur_flight,depth=answer[cur_flight.flight_no]
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
        mh.insert((start_city,None))   # (city,flight)
        while mh.top()!=None:
            cur_city,best_flight=mh.extract()

            if cur_city==end_city:
                break
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
                        mh.insert((flight.end_city,flight))
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
        mh.insert((start_city,None))   # (city,flight)
        while mh.top()!=None:
            cur_city,best_flight=mh.extract()

            if cur_city==end_city:
                break
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
                        mh.insert((flight.end_city,flight))
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
    