# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def split(self,num,start,end):
        if start>end:
            return None
        mid=start+(end-start)/2
        root=TreeNode(num[mid])
        root.left=self.split(num, start, mid-1)
        root.right=self.split(num, mid+1, end)  
        return root
    
    def sortedArrayToBST(self, num):  
        if len(num)==0:
            return None
        if len(num)==1:
            root=TreeNode(num[0])
            return root
        self.split(num, 0, len(num)-1)