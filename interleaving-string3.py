
class Solution(object):
    def __init__(self):
        self.counter = 0
    def isInterleave(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool

        """
        print self.counter
        self.counter += 1
        if len(s1) == 0:
            return s2 == s3
        elif len(s2) == 0:
            return s1 == s3
        else:
            if s1[0] == s3[0] and s2[0] == s3[0]:
                return self.isInterleave(s1[1:],s2,s3[1:]) or self.isInterleave(s1,s2[1:],s3[1:]) 
            elif s1[0] == s3[0]:
                return self.isInterleave(s1[1:],s2,s3[1:])
            elif s2[0] == s3[0]:
                return self.isInterleave(s1,s2[1:],s3[1:])
            else:
                return False
            
if __name__ == '__main__':
    s = Solution()
    '''
    s1 = "aabcc"
    s2 = "dbbca"
    s3 = 'aadbbcbcac'
    '''
    '''
    s1 = "db"
    s2 = "b"
    s3 = "cbb"
    '''
    
    s1 = "bbbbbabbbbabaababaaaabbababbaaabbabbaaabaaaaababbbababbbbbabbbbababbabaabababbbaabababababbbaaababaa"
    s2 = "babaaaabbababbbabbbbaabaabbaabbbbaabaaabaababaaaabaaabbaaabaaaabaabaabbbbbbbbbbbabaaabbababbabbabaab"
    s3 = "babbbabbbaaabbababbbbababaabbabaabaaabbbbabbbaaabbbaaaaabbbbaabbaaabababbaaaaaabababbababaababbababbbababbbbaaaabaabbabbaaaaabbabbaaaabbbaabaaabaababaababbaaabbbbbabbbbaabbabaabbbbabaaabbababbabbabbab"
    
    s1 = "a"
    s2 = ""
    s3 = "c"
    
    print s.isInterleave(s1,s2,s3)