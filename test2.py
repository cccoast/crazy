class Solution(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: void Do not return anything, modify matrix in-place instead.
        """
        
        rev = []
        if len(matrix):
            n,m = len(matrix),len(matrix[0])
            for i in range(m)[::-1]:
                rev.append([])
                last = rev[-1]
                for j in range(n)[::-1]:
                    last.append(matrix[j][i])
        rev = rev[::-1]
        a1,a2 = [],[]
        if m > n:
            for i in range(n):
                matrix[i][:] = rev[i][:]
            for i in range(abs(m-n)):
                matrix.pop()
        else:
            for i in range(m):
                matrix[i][:] = rev[i][:]
            for i in range(abs(m-n)):
                matrix.append(rev[m+i])
                
if __name__ == '__main__':
    s = Solution()
    m = [[1,2],[3,4]]
    s.rotate(m)
    print m