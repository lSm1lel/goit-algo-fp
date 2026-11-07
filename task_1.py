"""Завдання 1. Реверсування, сортування та злиття однозв'язних списків."""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def build_list(values):
    head = tail = None
    for value in values:
        node = Node(value)
        if head is None:
            head = node
        else:
            tail.next = node
        tail = node
    return head


def to_list(head):
    values = []
    while head is not None:
        values.append(head.data)
        head = head.next
    return values


def reverse_linked_list(head):
    """Змінює посилання next на місці та повертає новий початок списку."""
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous


def merge_sorted_lists(first, second):
    """Зливає два відсортовані списки, повторно використовуючи їхні вузли."""
    dummy = Node(None)
    tail = dummy
    while first is not None and second is not None:
        if first.data <= second.data:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next
        tail = tail.next
    tail.next = first if first is not None else second
    return dummy.next


def merge_sort(head):
    """Сортує список злиттям, не перетворюючи його на масив."""
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    return merge_sorted_lists(merge_sort(head), merge_sort(second))


def main():
    head = build_list([4, 2, 5, 1, 3])
    print("Початковий список:", to_list(head))
    head = reverse_linked_list(head)
    print("Після реверсування:", to_list(head))
    head = merge_sort(head)
    print("Після сортування:", to_list(head))
    first = build_list([1, 3, 5])
    second = build_list([2, 4, 6])
    merged = merge_sorted_lists(first, second)
    print("Злиття [1, 3, 5] та [2, 4, 6]:", to_list(merged))


if __name__ == "__main__":
    main()
