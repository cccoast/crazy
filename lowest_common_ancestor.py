
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def init(self):
        self.find = False
        self.node = None
        
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        self.init()
        self.dfs(root,p,q)
        return self.node
    
    def dfs(self,root,p,q):
        if self.find == True:
            return None
        val,left,right = 0,0,0
        if root == None:
            return 0
        elif root is p: 
            val = 1
        elif root is q: 
            val = 2
            
        right = self.dfs(root.right, p, q)
        left = self.dfs(root.left,p,q)
        print sorted([val,left,right])
        if self.find == False and (sorted([val,left,right]) == [0,1,2]):
            self.find = True
            self.node = root
        else:
            if self.find == False:
                return filter(lambda x:x!=0,(val,left,right))[0]
                
if __name__ == '__main__':
    sol = Solution()
    root = TreeNode(2)
    root.right = TreeNode(1)
    print sol.lowestCommonAncestor(root,root,root.right)