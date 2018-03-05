class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """
        print [min(i,c) for i,c in enumerate(sorted(citations,reverse = True))]
        print max(min(i,c) for i,c in enumerate(sorted(citations,reverse = True)))
        
#         c = sorted(citations,reverse = True)
#         l = len(c)
#         if not l:
#             return 0
#         for i in range(l):
#             if i + 1 > c[i] :
#                 return i - 1
#         return l
        
if __name__ == '__main__':
    s = Solution()
    print s.hIndex([1,2,3,4])