class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        
        from itertools import chain
        l = len(s)
        if l <= 1 or numRows == 1:
            return s
        re = [[] for i in range(numRows)]
        period = numRows*2 - 2
        for i in range(l):
            p = i%period
            if p <= numRows-1:
                re[p].append(s[i])
            else:
                re[(numRows-1)-(p-numRows+1)].append(s[i])
        return ''.join([i for i in chain(*re)])
    
if __name__ == '__main__':
    s = Solution()
    print s.convert("PAYPALISHIRING", 3)