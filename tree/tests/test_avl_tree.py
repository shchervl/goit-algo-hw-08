import pytest

from tree import build_tree, inorder, insert


def test_insert_single_node():
    root = insert(None, 42)
    assert root.key == 42
    assert root.left is None and root.right is None


def test_inorder_returns_sorted_keys():
    root = build_tree([20, 4, 26, 3, 9, 15, 30, 2])
    assert inorder(root) == [2, 3, 4, 9, 15, 20, 26, 30]


def test_insert_keeps_tree_balanced_when_input_sorted():
    root = build_tree(list(range(1, 16)))
    assert root.height <= 5


def test_duplicates_are_ignored():
    root = build_tree([5, 5, 5, 3, 3, 7])
    assert inorder(root) == [3, 5, 7]


def test_insert_none_raises():
    with pytest.raises(TypeError):
        insert(None, None)


def test_insert_string_raises():
    with pytest.raises(TypeError):
        insert(None, "abc")


def test_insert_bool_raises():
    with pytest.raises(TypeError):
        insert(None, True)


def test_failed_insert_leaves_tree_intact():
    root = insert(None, 10)
    with pytest.raises(TypeError):
        insert(root, "x")
    assert inorder(root) == [10]
