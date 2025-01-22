import pdb
import glob
import heap
import straw_hat
import treasure
import sys

sys.setrecursionlimit(10**6)
            
class Parser():
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.read_data()
        
    def read_data(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.data.append(line.strip())
    
    def parse(self):
        pass

class ParserTreasure(Parser):
    def parse(self):
        strin=[]
        m = int(self.data[0])
        treasury = straw_hat.StrawHatTreasury(m)
        for i in range(1, len(self.data)):
            try:
                query = self.data[i].split()
                query_type = query[0]
                if query_type == 'Add':
                    id, size, arrival_time = query[1], query[2], query[3]
                    # if query[1]=='1003':
                        # pdb.set_trace()
                    id = int(id)
                    size = int(size)
                    arrival_time = int(arrival_time)
            except:
                raise ValueError('Invalid Input')
            if query_type == 'Add':
                try:
                    treasure_obj = treasure.Treasure(id, size, arrival_time)
                    treasury.add_treasure(treasure_obj)
                    strin.append(f'Treasure {id} added to treasury')
                except:
                    strin.append(f"Cannot add treasure {id} to treasury")
            elif query_type == 'Get':
                # try:
                processed = treasury.get_completion_time()
                strin.append(f'Completion Time: {[(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed]}')
                # except:
                #     print('Cannot get completion time')
            else:
                raise ValueError('Invalid Input')
        return strin

class ParserHeap(Parser):
    def __init__(self, filename, comparison = lambda a, b: a<b):
        super().__init__(filename)
        self.comp = comparison
    
    def parse(self):
        strin=[]
        h = heap.Heap(self.comp, [])
        num = 0
        for i in range(len(self.data)):
            query = self.data[i].split()
            if query[0] == 'Insert':
                try:
                    h.insert(int(query[1]))
                    num += 1
                    strin.append(f'{query[1]} inserted')
                except:
                    strin.append(f'Cannot insert {query[1]}')
            elif query[0] == 'Extract':
                try:
                    strin.append(f'{h.extract()} extracted')
                    num -= 1
                except:
                    strin.append('Cannot extract')
            elif query[0] == 'Top':
                try:
                    strin.append(f'Top: {h.top()}')
                except:
                    strin.append('Cannot get top')
            elif query[0] == 'Print':
                try:
                    news=""
                    for i in range(num):
                        news+=str(h.extract())
                        news+=" "
                        num -= 1
                    news+='\n'
                    strin.append(news)
                except:
                    
                    strin.append('Cannot print')
            else:
                raise ValueError('Invalid Input')
        return strin

if __name__ == '__main__':
    with open("output.txt",'w') as f:

        f.write("----------tc_heap1.txt----------\n")
        parser = ParserHeap('tc_heap1.txt')
        output=parser.parse()
        for line in output:
            stringg=line+'\n'
            f.write(stringg)
        file_paths = glob.glob("tc_treasury*.txt")
        for file in file_paths:
            f.write(f"----------{file}----------\n")
            parser = ParserTreasure(file)
            output=parser.parse()
            for line in output:
                stringg=line+'\n'
                f.write(stringg)
            f.write('\n')
        f.write("END")