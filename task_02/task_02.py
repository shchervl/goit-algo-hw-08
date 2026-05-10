"""Task 02: find the sum of all values in an AVL tree."""

import random

from tree import build_tree, inorder


def tree_sum(root):
    """Return the sum of all keys in the tree.

    Visits every node exactly once → O(n). Empty tree returns 0.
    """
    if root is None:
        return 0
    return root.key + tree_sum(root.left) + tree_sum(root.right)


if __name__ == "__main__":
    values = random.choices(range(1, 50), k=10)
    root = build_tree(values)

    # Original values could have duplicates
    print(f"{'Original values for tree build:':<32} {values}")
    print(f"{'Tree (in-order):':<32} {inorder(root)}")

    print(f"{'Sum of all values:':<33}{tree_sum(root)}")
