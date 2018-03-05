# The isBadVersion API is already defined for you.
# @param version, an integer
# @return a bool
# def isBadVersion(version):
import numpy as np

last = 0
def isBadVersion(n):
    if n >= last:
        return True
    else:
        return False

def init(n):
    last = np.random.randint(1,n+1,1)[0]
    print 'last = ',last
    return last      

class Solution(object):
    
    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """

        start,mid,end = 1,int(n/2),n
        result = 0
        while True:
            bs = isBadVersion(start)
            bm = isBadVersion(mid)
#             print start,mid,end
            if bs == True:
                result = start
                break
            elif bm == False:
                start = mid
                mid = int((start + end)/2 )
            elif bm == True:
                end = mid
                mid = int((start + end)/2 )
                
            if mid == start:
                if isBadVersion(start):
                    result = start
                else:
                    result = end
                break
        return result
    
if __name__ == '__main__':
    n = 2
    s = Solution()
    last = init(n)
    print s.firstBadVersion(n)