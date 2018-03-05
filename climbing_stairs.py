class Solution(object):
    '''
    A*(x1,x2) = (x1,x2)*(l1,l2)
    '''
    
    def eig_init(self):
        self.eigval = [1.61803399,-0.61803399]
        self.eigvector = [[0.85065080835203988, -0.52573111211913348],\
                          [ 0.52573111211913348,  0.85065080835203988]]
        self.eigvectorT = [[0.85065080835203988, 0.52573111211913348],\
                          [ -0.52573111211913348,  0.85065080835203988]]
    
    def matrix_mul(self,x,y):
        y0 = x[0][0] * y[0][0] + x[0][1] * y[1][0]
        y1 = x[0][0] * y[0][1] + x[0][1] * y[1][1]
        y2 = x[1][0] * y[0][0] + x[1][1] * y[1][0]
        y3 = x[1][0] * y[0][1] + x[1][1] * y[1][1]
        return [[y0,y1],[y2,y3]]
        
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        self.eig_init()
        mid = [[1.6180339887498949**n ,0.000],\
              [0.0000,(-0.61803398874989479)**n]]
        nsquare = self.matrix_mul( self.matrix_mul(self.eigvector, mid), self.eigvectorT)
        print nsquare
        return int(nsquare[0][0] + 0.000000000001)

                                
if __name__ == '__main__':
    s = Solution()
    print s.climbStairs(2)