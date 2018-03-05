class Solution:
    def reverseWords(self, s):
        return ' '.join(s.split()[::-1])
    
    def maxPoints(self, points):
        if len(points) == 0:
            return 0
        ans = 0
        num_of_points = len(points)
        for i in range(num_of_points):
            counter = {}
            x0 = points[i].x
            y0 = points[i].y
            du = 0
            inf = 0
            for j in range(num_of_points):
                x1 = points[j].x
                y1 = points[j].y
                if i == j:
                    continue
                elif x1 == x0 and y1 == y0:
                    du += 1
                elif x1 == x0:
                    inf += 1
                else:
                    k = float(y1 - y0) / float(x1 - x0)
                    if k in counter.keys():
                        counter[k] += 1
                    else:
                        counter[k] = 1
            ans = inf + du if inf + du > ans else ans
            for key,value in counter.iteritems():
                if value + du > ans:
                    ans = value + du
        return ans + 1

class Point(object):
    def __init__(self, a=0, b=0):
        self.x = a
        self.y = b
         
if __name__ == '__main__':
    sol = Solution()
    l = []
    l.append(Point(1,1))
    l.append(Point(1,1))
#     l.append(Point(3,3))
    print sol.maxPoints(l)
#     print sol.reverseWords('the sky is blue')