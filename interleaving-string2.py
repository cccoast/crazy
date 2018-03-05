class Solution(object):
    
    def init(self,s1,s2,s3):
        
        self.cache = []
        for i in range(len(s1) + 1):
            self.cache.append([-1] * (len(s2)+1))
        self.cache[0][0] = 1
        
        for i in range(1,len(s1)+1):
            self.cache[i][0] = int( s1[:i] == s3[:i] )
        for i in range(1,len(s2)+1):
            self.cache[0][i] = int( s2[:i] == s3[:i] )
     
    def isInterleave(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """
        self.init(s1,s2,s3)
        return bool(self.deepFirstSearch(s1,s2,s3))
    
    def deepFirstSearch(self,s1,s2,s3):
    
        l1,l2,l3 = len(s1),len(s2),len(s3)
        if l1 + l2 != l3:
            self.cache[l1][l2] = 0
            return self.cache[l1][l2]
        if self.cache[l1][l2] != -1:
            return self.cache[l1][l2]
        else:
#             print s1,s2,s3
            if l1 != 0 and s1[-1] == s3[-1]:
                reached = self.deepFirstSearch(s1[:-1],s2,s3[:-1])
                self.cache[l1][l2] = int(reached)
                if reached:
                    return self.cache[l1][l2]
            if l2 != 0 and s2[-1] == s3[-1]:
                reached = self.deepFirstSearch(s1,s2[:-1],s3[:-1])
                self.cache[l1][l2] = int(reached)
                if reached:
                    return self.cache[l1][l2]
            self.cache[l1][l2] = 0
            return  self.cache[l1][l2]
        
if __name__ == '__main__':
    s = Solution()
    
    s1 = "aabcc"
    s2 = "dbbca"
    s3 = 'aadbbcbcac'
    
    '''
    s1 = "db"
    s2 = "b"
    s3 = "cbb"
    '''
    '''
    s1 = "bbbbbabbbbabaababaaaabbababbaaabbabbaaabaaaaababbbababbbbbabbbbababbabaabababbbaabababababbbaaababaa"
    s2 = "babaaaabbababbbabbbbaabaabbaabbbbaabaaabaababaaaabaaabbaaabaaaabaabaabbbbbbbbbbbabaaabbababbabbabaab"
    s3 = "babbbabbbaaabbababbbbababaabbabaabaaabbbbabbbaaabbbaaaaabbbbaabbaaabababbaaaaaabababbababaababbababbbababbbbaaaabaabbabbaaaaabbabbaaaabbbaabaaabaababaababbaaabbbbbabbbbaabbabaabbbbabaaabbababbabbabbab"
    '''
    '''
    s1 = "aacaac"
    s2 = "aacaaeaac"
    s3 = "aacaacaaeaacaac"
    '''
    '''
    s1 = "a"
    s2 = ""
    s3 = "c"
    '''
    '''
    s1 = "ab"
    s2 = "bc"
    s3 = "babc"
    '''
    print s.isInterleave(s1,s2,s3)