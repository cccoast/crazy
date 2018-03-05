class Solution(object):
    def numSquares(self, n):
        """
        :type n: int
        :rtype: int
        """
        sq = []
        i = 1
        while i*i <= n:
            sq.append(i*i)
            i += 1
        minium = [100000000] * (n+1)
        for i in sq:
            minium[i] = 1
        for i in xrange(1,n):
            j = 1 
            while j*j + i <= n:
                if minium[i+j*j] == 1 or minium[i+j*j] == 2:
                    j += 1
                    continue
                minium[i+j*j] = min(minium[i+j*j] , (minium[i] + 1))
                j += 1
        return minium[n]

if __name__ == '__main__':
    s = Solution()
    print s.numSquares(12)