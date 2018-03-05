class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        re = []
        nums = sorted(nums)
        if nums[0] != nums[1]:
            re.append(nums[0])
        for i in range(1,len(nums)-1):
            if nums[i] != nums[i-1] and nums[i] != nums[i+1]:
                re.append(nums[i])
        if nums[-1] != nums[-2]:
            re.append(nums[-1])
        return re
            
if __name__ == '__main__':
    sol = Solution()
    print sol.singleNumber([1, 2, 1, 3, 2, 5])