class Solution(object):
    
    def init(self):
        self.result = []
        self.dcheck = set()
    
    def threeSum(self,nums,target,init):
        nl = len(nums)
#         print nums
        for j in range(nl):
            if init + nums[j] * 3 > target:
                return 
            l,r = j+1,nl-1
            while l < r: 
#                 print init,nums[j],nums[l],nums[r]
                sum4 = nums[j] + nums[l] + nums[r] + init
                if sum4 == target:
                    t = tuple([init,nums[j],nums[l],nums[r]]) 
                    if t not in self.dcheck:
                        self.result.append([init,nums[j],nums[l],nums[r]])
                        self.dcheck.add(t)
                    l += 1
                elif sum4 < target:
                    l += 1
                elif sum4 > target:
                    r -= 1
        
    def fourSum(self, nums,target):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        self.init()
        nums = sorted(nums)
        l = len(nums)
        if 0 < l < 4:
            return self.result
        for i in range(l):
            if nums[i] * 4 > target:
                break
            self.threeSum(nums[i+1:],target,nums[i])
        return self.result
                            
if __name__ == '__main__':
    s = Solution()
    print s.fourSum([-1,0,1,2,-1,-4],-1)
#     print s.fourSum([-3,-2,-1,0,0,1,2,3],0)
    