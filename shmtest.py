class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """
        l = len(citations)
        left,right = 0,l - 1;
        while (left <= right):
            mid = int( (right - left )/2 ) + left
            if (citations[mid] == l - mid):
                return l - mid
            elif (citations[mid] > l - mid):
                right = mid - 1
            else:
                left = mid + 1
        return l - left

if __name__ == '__main__':
    s = Solution()
    print s.hIndex([0,1])