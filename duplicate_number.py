class Solution(object):
    def findDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        a = sorted(nums)
        for i in range(len(nums)-1):
            if a[i] == a[i+1]:
                return a[i]
        '''   
        a = set()
        for i in nums:
            if i in a:
                return i
            else:
                a.add(i)
        '''
        
        
if __name__ == '__main__':
    s = Solution()
    a = range(100)
    a.append(99)
    print s.findDuplicate(a)
    
    
    
    