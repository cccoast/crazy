# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def __init__(self):
        self.counter = 0   
    def maxDepth(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if root == None:
            return 0
        else:
            print self.counter,root.val
            self.counter += 1
            return max(self.maxDepth(root.left),self.maxDepth(root.right)) + 1
        
if __name__ == '__main__':
    s = Solution()
    print s.maxDepth()