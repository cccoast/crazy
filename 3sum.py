class Solution(object):
    def threeSumClosest(self, nums,target):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        nums = sorted(nums)
        minn  = 10000000
        l = len(nums)
        result = 0
        for i in range(l):
            for j in range(i+1,l):
                sum2 = nums[i] + nums[j]
                if sum2 > minn:
                    return result
                for k in range(j+1,l):
                    t = abs(sum2 + nums[k] - target)
                    if  t < minn:
                        minn = t
                        result = sum2 + nums[k]
                    if sum2 > 0:
                        break
        return result
    
if __name__ == '__main__':
    s = Solution()
    print s.threeSumClosest([0,0,0],1)