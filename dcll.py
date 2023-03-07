"""
Doubly Circular Linked List, according to:
https://www.askpython.com/python/examples/doubly-circular-linked-list
in combination with my phD's algorithm's requirements
"""
from typing import Optional


class DCLLNode:
    def __init__(self, data=None):
        self._data = data
        self._prev = self
        self._next = self

    def __repr__(self):
        return f"{self.data}"

    def __str__(self):
        return f"Doubly Circular Linked List's Node ({self.data})"

    def __iter__(self):
        return DCLL(self)

    def __eq__(self, other):
        if not isinstance(other, DCLLNode):
            return False
        return (self.data, self.prev, self.next) == (other.data, other.prev, other.next)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d):
        self._data = d

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, node):
        self._prev = node

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node


class DCLL:
    def __init__(self, node=None):
        self._head: Optional[DCLLNode] = node
        self._count = 0
        self._tail: Optional[DCLLNode] = node

    def __repr__(self):
        string = ""

        if self.head is None:
            string += "Doubly Circular Linked List is empty"
            return string

        string += f"Doubly Circular Linked List:\n{self.head.data}"
        temp = self.head.next
        while temp != self.head:
            string += f" -> {temp.data}"
            temp = temp.next
        return string

    def __next__(self):
        self._n += 1
        if self._current is None or self._n > self.count:
            raise StopIteration
        else:
            temp = self._current
            self._current = self._current.next
            return temp

    def __iter__(self):
        self._n = 0
        self._current = self.head
        return self

    def __reverse__(self):
        ...

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("List index must be an integer >= 0")
        elif index < 0 or index >= self.count:
            raise IndexError("Index out of range")
        else:
            temp = self.head
            for i in range(self.count):
                if i == index:
                    return temp
                temp = temp.next
            return None

    def __setitem__(self, index, item):
        if not isinstance(index, int):
            raise TypeError("List index must be an integer >= 0")
        elif index > self.count or index < 0:
            raise IndexError("Index out of range")
        if not isinstance(item, DCLLNode):
            raise TypeError("An item must be a DCLLNode")

        if self.head is None:
            self.head = item
            self.count = 1
            return self.get(self.count - 1)

        temp = self.head
        if index == 0:
            temp = temp.prev
        else:
            for _ in range(index - 1):
                temp = temp.next

        temp.next.prev = item
        temp.next.prev.next, temp.next.prev.prev = temp.next, temp
        temp.next = temp.next.prev
        if index == 0:
            self.head = self.head.prev
        self.count += 1
        self.tail = self.head.prev
        return self.get(index)

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, node):
        self._head = node

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, c):
        self._count = c

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, node):
        self._tail = node

    def append(self, data):
        return self.insert(data, self.count)

    def insert(self, data, index):
        if (index > self.count) or (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.head is None:
            self.head = DCLLNode(data)
            self.count = 1
            return self.get(self.count - 1)

        temp = self.head
        if index == 0:
            temp = temp.prev
        else:
            for _ in range(index - 1):
                temp = temp.next

        temp.next.prev = DCLLNode(data)
        temp.next.prev.next, temp.next.prev.prev = temp.next, temp
        temp.next = temp.next.prev
        if index == 0:
            self.head = self.head.prev
        self.count += 1
        self.tail = self.head.prev
        return self.get(index)

    def remove(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.count == 1:
            self.head = None
            self.count = 0
            self.tail = None
            return None

        target = self.head
        for _ in range(index):
            target = target.next

        if target is self.head:
            self.head = self.head.next

        target.prev.next, target.next.prev = target.next, target.prev
        self.count -= 1
        self.tail = self.head.prev
        return self.get(index - 1)

    def index(self, data, from_index=0, from_data=None):
        if from_data:
            temp = from_data
        else:
            temp = self.head
        for i in range(from_index, self.count):
            if temp.data == data:
                return i
            temp = temp.next
        raise ValueError(f"No {data} found on the intersect pts list")

    def get(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp.data

    def size(self):
        return self.count

    def display(self):
        print(self)

    def set_order(self, order_list):
        """
        Sets the order od DCLL Nodes according to order_list,
        where the DCLLNode.data items are already sorted.
        """
        if self.count == 0:
            return None
        elif self.count == 1:
            return self.head
        elif self.count == 2:
            self.head = self.tail
            self.tail = self.head.next
            return self.head
        else:
            from_data = self.head.prev
            for i, item in enumerate(order_list):
                if i < self.count - 1:
                    current_index = self.index(item.data, i, from_data.next)
                    from_data = self.move(item, current_index, i)
                if i == 0:
                    self.head = item
            self.tail = self.head.prev
            return self.head

    def move(self, item, from_index, to_index):
        if (from_index > self.count) or (from_index < 0):
            raise ValueError(f"Index out of range: {from_index}, size: {self.count}")
        if (to_index > self.count) or (to_index < 0):
            raise ValueError(f"Index out of range: {to_index}, size: {self.count}")

        if from_index == to_index:
            return item
        else:
            # removing data from current index
            item.prev.next = item.next
            item.next.prev = item.prev

            # searching for target place
            index_difference = to_index - from_index
            curr_item = item
            if index_difference > 0:
                for _ in range(index_difference - 1):
                    curr_item = curr_item.next
            else:
                for _ in range(-index_difference + 1):
                    curr_item = curr_item.prev

            return self.set_item_after_item0(curr_item, item)

    def set_item_after_item0(self, item0, item):
        item.next = item0.next
        item.prev = item0
        item0.next.prev = item
        item0.next = item
        return item

    def remove_repeated_data(self, count):
        c = count
        if self.head and self.head is not self.head.next:
            p = self.head
        else:
            return c
        while True:
            t = p.next
            while t is not self.head:
                if t.data == p.data:
                    if p is self.head:
                        self.head = self.head.next

                    t.prev.next, t.next.prev = t.next, t.prev
                    self.count -= 1
                    self.tail = self.head.prev
                    c -= 1
                else:
                    t = t.next
            p = p.next
            if p is self.head:
                break

        return c

    def find_node_by_data(self, d):
        if self.head:
            t = self.head
            while True:
                if t.data is d:
                    return t
                t = t.next
                if t is self.head:
                    break
        return None

    def delete_node(self, n):
        if self.head:
            if n is self.head:
                self.head = self.head.next
            n.prev.next, n.next.prev = n.next, n.prev
            self.count -= 1
            self.tail = self.head.prev

    def clear_list(self):
        if self.head:
            self.head = None
            self.tail = None
            self.count = 0
        return True
    
