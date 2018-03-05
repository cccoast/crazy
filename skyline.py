class Solution(object):

    def getSkyline(self, buildings):
        """
        :type buildings: List[List[int]]
        :rtype: List[List[int]]
        """
        xs = [(i[0],i[2],0) for i in buildings]
        ys = [(i[1],i[2],1) for i in buildings]
        ys.extend(xs)
        points = list(set(ys))
        length = len(points)
        height = [0] * length
        for i,v in enumerate(points):
            index[v] = i
        for ibuild in buildings:
            l = index[ibuild[0]]
            r = index[ibuild[1]]
#             print ibuild,l,r
            while l < r:
                height[l] = height[l] if height[l] > ibuild[2] else ibuild[2]
                l += 1
#             print 'height',self.height
        h = 0
        re = []
        for i in range(length):
            if height[i] != h:
                re.append([points[i],height[i]])
                h = height[i]
        print 1
        return re
        
if __name__ == '__main__':
    buildings = [ [2,9,10], [3,7,15], [5,12,12], [15,20,10], [19,24,8] ]
#    buildings = [ [1,10,2], [1,10,3], [1,10,4], [1,10,5], [1,10,6],]
    s = Solution()
    print s.getSkyline(buildings)
    