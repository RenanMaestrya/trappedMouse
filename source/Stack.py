class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if not self.is_empty():
            popped_item = self.top.data
            self.top = self.top.next
            return popped_item
        return None

    def size(self):
        current = self.top
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def peek(self):
        if not self.is_empty():
            return self.top.data

    def contains(self, item):
        current = self.top
        while current:
            if current.data == item:
                return True
            current = current.next
        return False    
    
    def reverse(self):
        reversed_stack = Stack()
        current = self.top
        while current:
            reversed_stack.push(current.data)
            current = current.next
        return reversed_stack
    
