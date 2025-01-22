from hash_table import *

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        # assert isinstance(texts, list) and isinstance(book_titles, list), "Invalid input" ################################################
        self.books=merge_sort(list(zip(book_titles,texts)))
        
        for i in range(len(self.books)):
            self.books[i]=(self.books[i][0],merge_sort(self.books[i][1]))

        self.unique_words = [[] for _ in range(len(self.books))]

        for i in range(len(self.books)):
            words=self.books[i][1]
            if not words:
                continue
            self.unique_words[i].append(words[0])
            for j in range(1,len(words)):
                if words[j]!=words[j-1]:
                    self.unique_words[i].append(words[j])
                
    def distinct_words(self, book_title):
        left=0
        right=len(self.books)-1
        while left<=right:
            mid=(left+right)//2
            if self.books[mid][0]==book_title:
                break
            elif self.books[mid][0]<book_title:
                left=mid+1
            else:
                right=mid-1
        else:
            return None
        return self.unique_words[mid]
    
    def count_distinct_words(self, book_title):
        left=0
        right=len(self.books)-1
        while left<=right:
            mid=(left+right)//2
            if self.books[mid][0]==book_title:
                break
            elif self.books[mid][0]<book_title:
                left=mid+1
            else:
                right=mid-1
        else:
            return None
        return len(self.unique_words[mid])
    
    def search_keyword(self, keyword):
        booklist=[]
        for i in range(len(self.unique_words)):
            left=0
            right=len(self.unique_words[i])-1
            while left<=right:
                mid=(left+right)//2
                if self.unique_words[i][mid]==keyword:
                    booklist.append(self.books[i][0])
                    break
                elif self.unique_words[i][mid]<keyword:
                    left=mid+1
                else:
                    right=mid-1
        return booklist
                
    
    def print_books(self):
        for i in range(len(self.books)):
            rep=f"{self.books[i][0]}: " + " | ".join(self.unique_words[i])
            print(rep)
            

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        if name=="Jobs":
            self.collision_type="Chain"
        elif name=="Gates":
            self.collision_type="Linear"
        else:
            assert name=="Bezos", "Invalid name"
            self.collision_type="Double"
        self.params=params
        if name=="Jobs":
            self.hash_map=HashMap("Chain",params)
        elif name=="Gates":
            self.hash_map=HashMap("Linear",params)
        else:
            # assert name=="Bezos", "Invalid name" ################################################
            self.hash_map=HashMap("Double",params)
        self.filled_books=[]
    def add_book(self, book_title, text):
        hash_set=HashSet(self.collision_type,self.params)
        for word in text:
            hash_set.insert(word)
        self.hash_map.insert((book_title,hash_set))
        self.filled_books.append((book_title,hash_set))
    
    def distinct_words(self, book_title):
        words:HashSet=self.hash_map.find(book_title)
        if self.collision_type=="Chain":
            returning=[]
            for list in words.list:
                if list!=None:
                    for word in list:
                        returning.append(word)
            return returning
        return [word for word in words.list if word!=None]

    
    def count_distinct_words(self, book_title):
        words:HashSet=self.hash_map.find(book_title)
        return words.element_count
    
    def search_keyword(self, keyword):
        books=[]
        for tup in self.filled_books:
            # assert isinstance(tup[1],HashSet), "Invalid input" ################################################
            if tup[1].find(keyword):
                books.append(tup[0])
        return books
    
    def print_books(self):        
        for tupl in self.filled_books:
            if tupl!=None:
                print(tupl[0],end="")
                print(":", tupl[1].__str__())
            


def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    def merge(left, right, key):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return merge(left, right, key)
