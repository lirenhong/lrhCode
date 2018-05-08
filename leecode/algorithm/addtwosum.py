# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def addTwoNumbers(self, l1, l2):
        head, p1, p2 = ListNode(0), l1, l2
        tail = head
        carry = 0
        while p1 and p2:
            num = p1.val + p2.val + carry
            if num > 9:
                num = num - 10
                carry = 1
            else:
                carry = 0

            tail.next = ListNode(num)
            tail = tail.next
            p1 = p1.next
            p2 = p2.next

        if p2:
            p1 = p2
        while p1:
            num = p1.val + carry
            if num > 9:
                num = num - 10
                carry = 1
            else:
                carry = 0
            tail.next = ListNode(num)
            tail = tail.next
            p1 = p1.next

        if carry:
            tail.next = ListNode(carry)
            tail = tail.next
        tail.next = None
        return head.next

if __name__ == "__main__":
    l1 = ListNode(2)
    l1.next = ListNode(4)
    l1.next.next = ListNode(3)

    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)



