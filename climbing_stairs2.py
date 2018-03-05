class Solution(object):
    '''
    A*(x1,x2) = (x1,x2)*(l1,l2)
    '''
    
    def matrix_mul(self,x,y):
        y0 = x[0][0] * y[0][0] + x[0][1] * y[1][0]
        y1 = x[0][0] * y[0][1] + x[0][1] * y[1][1]
        y2 = x[1][0] * y[0][0] + x[1][1] * y[1][0]
        y3 = x[1][0] * y[0][1] + x[1][1] * y[1][1]
        return [[y0,y1],[y2,y3]]
    
    def binary_divide(self,n):
        if n == 1:
            return [[1,1],[1,0]]
        if n == 2:
            return self.matrix_mul([[1,1],[1,0]], [[1,1],[1,0]])
        else:
            return self.matrix_mul( self.binary_divide(n/2) , self.binary_divide(n-n/2) )
            
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        return self.binary_divide(n)[0][0]
                                
if __name__ == '__main__':
    s = Solution()
    print s.climbStairs(38)