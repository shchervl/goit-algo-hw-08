"""Task 01: find the smallest value in an AVL tree."""

import random

from tree import build_tree, inorder


def find_min(root):
    """Return the smallest key in the tree.

    Walks left from the root; the leftmost node holds the minimum (BST property).
    Runs in O(h), which is O(log n) on an AVL tree.
    Raises ValueError if the tree is empty.
    """
    if root is None:
        raise ValueError("tree is empty")
    node = root
    while node.left is not None:
        node = node.left
    return node.key


if __name__ == "__main__":
    values = random.sample(range(1, 100), 10)
    print(f"{'Used values for tree build:':<30} {values}")

    root = build_tree(values)

    print(f"{'Tree (in-order):':<30} {inorder(root)}")
    print(f"{'Minimum value in the tree:':<30} {find_min(root)}")
