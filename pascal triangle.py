class Solution:

    def generate(self, numRows):
        a = []
        if numRows <= 0:
            return a
        else:
            for i in range(numRows):
                b = []
                if i == 0:
                    b.append(1)
                else:
                    b.append(1)
                    for j in range(i-1):
                        b.append(a[i-1][j] + a[i-1][j+1])
                    b.append(1)
                a.append(b)
            return a
        
if __name__ == '__main__':
    sol = Solution()
    print sol.generate(10)