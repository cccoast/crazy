class Solution(object):
    
                
    def isInterleave(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """
        l1,l2,l3 = len(s1),len(s2),len(s3)
        if l1 + l2 != l3:
            return False
        path = []
        for i in range(l1 + 1):
            path.append([0] * (l2+1))
        path[0][0] = 1
        for i in range(l1):
            if s3[:i+1] == s1[:i+1]:
                path[i+1][0] = 1
        for j in range(l2):
            if s3[:j+1] == s2[:j+1]:
                path[0][j+1] = 1
        for i in range(1,l1+1):
            for j in range(1,l2+1):
                if path[i-1][j] == 1:
                    if s3[i+j-1] == s1[i-1]:
                        path[i][j] = 1
                        continue
                if path[i][j-1] == 1:
                    if s3[i+j-1] == s2[j-1]:
                        path[i][j] = 1
                        continue
#         print path
        return bool(path[l1][l2])
                
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