class Flight:
    def __init__(self, flight_no, start_city, departure_time, end_city, arrival_time, fare):
        """ Class for the flights

        Args:
            flight_no (int): Unique ID of each flight
            start_city (int): The city no. where the flight starts
            departure_time (int): Time at which the flight starts
            end_city (int): The city no where the flight ends
            arrival_time (int): Time at which the flight ends
            fare (int): The cost of taking this flight
        """
        self.flight_no = flight_no
        self.start_city = start_city
        self.departure_time = departure_time
        self.end_city = end_city
        self.arrival_time = arrival_time
        self.fare = fare
        self.dep_city:"City" = None
        self.arr_city:"City" = None

    def __repr__(self):
        return f"Flight {self.flight_no}: {self.start_city}->{self.end_city} {self.departure_time}->{self.arrival_time} {self.fare}"
        
    def __lt__(self,other):
        return self.flight_no<other.flight_no
"""
If there are n flights, and m cities:

1. Flight No. will be an integer in {0, 1, ... n-1}
2. Cities will be denoted by an integer in {0, 1, .... m-1}
3. Time is denoted by a non negative integer - we model time as going from t=0 to t=inf
"""

class City:
    def __init__(self, city_no:int):
        """Class for the cities

        Args:
            city_no (int): The city no.
        """
        self.city_no = city_no
        self.arriving_flights:list[Flight] = []
        self.departing_flights:list[Flight] = []

    def __repr__(self):
        return f"City {self.city_no}, arriving_flights={self.arriving_flights}, departing_flights={self.departing_flights}"
    
