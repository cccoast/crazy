class Solution(object):
    def minPathSum(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        if len(grid) == 0:
            return 0
        m,n = len(grid),len(grid[0])
        re = []
        for i in range(m+2):
            re.append([0] * (n+2))
        re[0][0] = grid[0][0]
        for i in range(1,m):
            re[i][0] += re[i-1][0] + grid[i][0]
        for i in range(1,n):
            re[0][i] += re[0][i-1] + grid[0][i]
        for i in range(1,m):
            for j in range(1,n):
                re[i][j] += min(re[i-1][j] , re[i][j-1]) + grid[i][j]
        print re
        return re[m-1][n-1]
        
if __name__ == '__main__':
    s = Solution()
    print s.minPathSum([[1,2],[1,1]])