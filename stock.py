class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if len(prices) > 0:
            maxx = 0
            prev_low = prices[0]
            for p in prices:
                if p < prev_low:
                    prev_low = p
                else:
                    maxx = max(p - prev_low,maxx)
            return maxx
        else:
            return 0
        
if __name__ == '__main__':
    sol = Solution()
    print sol.maxProfit([2,1])