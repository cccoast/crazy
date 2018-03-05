class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """
        while num >= 10:
            b = 0
            while num > 0:
                b += num%10
                num /= 10
            num = b
        return num

if __name__ == '__main__':
    s = Solution()
    print s.addDigits(10)