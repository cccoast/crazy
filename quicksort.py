import numpy as np
import time
a = np.random.randint(0,100,10000)
# a = [36,0,22,49,90]
def quicksort(start,end):
    if start >= end:
        return 
    else:
#         mid = (start + end)/2
#         a[start],a[mid] = a[mid],a[start]
        v = a[start]
        l,r = start,end
        while l < r:
            while a[r] > v and l < r:
                r -= 1
            if l < r:
                a[l],a[r] = a[r],a[l]
                l += 1
                
            while a[l] < v and l < r:
                l += 1
            if l < r:
                a[r],a[l] = a[l],a[r]
                r -= 1
#         print a
        quicksort(start,l-1)
        quicksort(l+1,end)
        return
print a
start = time.time()
quicksort(0,len(a)-1)
end = time.time()
print end - start,'second'