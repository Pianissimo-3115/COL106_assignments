a=[]
b=[]
with open("test1.txt", 'r') as f:
    a=f.readlines()
with open("test2.txt",'r') as g:
    b=g.readlines()
for i in range(len(a)):
    if a[i]!=b[i]:
        print(f"At line {i}: {a[i]}!={b[i]}")
print("DONE")
