class Solution(object):
    def map(self,s):
        a = dict()
        no = 0
        pattern = []
        for i in s:
            if not a.has_key(i):
               pattern.append(no)
               a[i] = no
               no += 1
            else:
                pattern.append(a[i])
        return pattern  
    def wordPattern(self, pattern, str):
        """
        :type pattern: str
        :type str: str
        :rtype: bool
        """
        p1 = self.map(pattern)
        p2 = self.map(str.split())
        return p1 == p2

        
if __name__ == '__main__':
    s = Solution()
    print s.wordPattern("abba","dog cat cat dog")