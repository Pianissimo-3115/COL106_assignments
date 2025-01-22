a="series"
sum=0
for i in range(len(a)):
    sum+=(ord(a[i])-ord('a'))*(40**i)
newsum=0
for i in range(len(a)):
    newsum+=(ord(a[i])-ord('a'))*(35**i)
i=0
newsum=17-newsum%17
print(newsum)
while True:
    if (sum+i*newsum)%37==5:
        print(i)
        break
    i+=1
print(sum%37)