"""Shared AVL tree implementation used by every task in this homework.

This is a classical BST/AVL that models a mathematical **set** of keys:
each value is present at most once. Re-inserting an existing key is a
no-op (see `insert` — duplicates are silently ignored).

If multiset/bag semantics are ever needed (i.e. counting how many times
each value was inserted), extend `AVLNode` with a `count` field and
increment it on the duplicate branch in `insert` rather than changing
the tree shape.
"""


class AVLNode:
    """Node of an AVL tree. Stores a key plus its subtree height."""

    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


def _height(node):
    """Return the height of a node, or 0 if the node is None."""
    return node.height if node else 0


def _current_balance(node):
    """Return left/right balance factor: >1 means left-heavy, <-1 right-heavy."""
    return _height(node.left) - _height(node.right) if node else 0


def _update_height(node):
    """Recalculate a node's height from its children. Call after structural changes."""
    node.height = 1 + max(_height(node.left), _height(node.right))


def _rotate_right(y):
    """Right rotation around `y`. Used to fix a left-heavy imbalance."""
    x = y.left
    t2 = x.right
    x.right = y
    y.left = t2
    _update_height(y)
    _update_height(x)
    return x


def _rotate_left(x):
    """Left rotation around `x`. Used to fix a right-heavy imbalance."""
    y = x.right
    t2 = y.left
    y.left = x
    x.right = t2
    _update_height(x)
    _update_height(y)
    return y


def insert(root, key):
    """Insert `key` into the AVL tree and return the (possibly new) root.

    The tree models a mathematical set, so duplicates are silently ignored
    (the existing node is returned unchanged). Non-numeric keys raise
    TypeError. After inserting, the tree is rebalanced via single or
    double rotations so that every node's balance factor stays in
    {-1, 0, 1}.
    """
    if not isinstance(key, (int, float)) or isinstance(key, bool):
        raise TypeError(f"key must be int or float, got {type(key).__name__}")
    if root is None:
        return AVLNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    _update_height(root)
    balance = _current_balance(root)

    # Left-Left: left-heavy and inserted into left child's left subtree.
    if balance > 1 and key < root.left.key:
        return _rotate_right(root)
    # Right-Right: right-heavy and inserted into right child's right subtree.
    if balance < -1 and key > root.right.key:
        return _rotate_left(root)
    # Left-Right: left-heavy but inserted into left child's right subtree.
    if balance > 1 and key > root.left.key:
        root.left = _rotate_left(root.left)
        return _rotate_right(root)
    # Right-Left: right-heavy but inserted into right child's left subtree.
    if balance < -1 and key < root.right.key:
        root.right = _rotate_right(root.right)
        return _rotate_left(root)

    return root


def inorder(node):
    """Return all keys in ascending order via in-order traversal (left, root, right)."""
    if node is None:
        return []
    return inorder(node.left) + [node.key] + inorder(node.right)


def build_tree(values):
    """Convenience helper: build an AVL tree from an iterable of keys."""
    root = None
    for value in values:
        root = insert(root, value)
    return root
