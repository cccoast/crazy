import numpy as np
import time

b = np.random.randint(0,100,1000)
def quicksort(a,start,end):
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
        quicksort(a,start,l-1)
        quicksort(a,l+1,end)
        return
    
def bubble_sort(array):
    l = len(array)
    for i in range(l):
        for j in range(l-i-1):
            if array[j] > array[j+1]:
                array[j],array[j+1] = array[j+1],array[j]
start = time.time()
bubble_sort(b)
end = time.time()
print end-start,'second'