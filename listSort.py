class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def sortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        a = []
        if head == None:
            return head
        while head:
            a.append(head.val)
            head = head.next
        a = sorted(a)
        head = ListNode(a[0])
        iter = head
        for i in range(1,len(a)):
            iter.next = ListNode(a[i])
            iter = iter.next
        return head
'''
class Solution:
    # @param head, a ListNode
    # @return a ListNode
    def sortList(self, head):
        if head is None or head.next is None:
            return head
        mid = self.getMiddle(head)
        rHead = mid.next
        mid.next = None
        return self.merge(self.sortList(head), self.sortList(rHead))

    def merge(self, lHead, rHead):
        dummyNode = ListNode(0)
        dummyHead = dummyNode
        while lHead and rHead:
            if lHead.val < rHead.val:
                dummyHead.next = lHead
                lHead = lHead.next
            else:
                dummyHead.next = rHead
                rHead = rHead.next
            dummyHead = dummyHead.next
        if lHead:
            dummyHead.next = lHead
        elif rHead:
            dummyHead.next = rHead
        return dummyNode.next

    def getMiddle(self, head):
        if head is None:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow
'''
if __name__ == '__main__':
    a = ListNode(2)
    a.next = ListNode(1)
    s = Solution()
    c = a
    while a:
        print a.val
        a = a.next
    b = s.sortList(c)
    while b:
        print b.val
        b = b.next