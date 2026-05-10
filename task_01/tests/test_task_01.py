import pytest

from tree import build_tree, insert
from task_01 import find_min


def test_find_min_single_node():
    root = insert(None, 42)
    assert find_min(root) == 42


def test_find_min_among_multiple_values():
    root = build_tree([20, 4, 26, 3, 9, 15, 30, 2])
    assert find_min(root) == 2


def test_find_min_already_sorted():
    root = build_tree([1, 2, 3, 4, 5])
    assert find_min(root) == 1


def test_find_min_reverse_sorted():
    root = build_tree([5, 4, 3, 2, 1])
    assert find_min(root) == 1


def test_find_min_with_negatives():
    root = build_tree([0, -5, 10, -100, 7])
    assert find_min(root) == -100


def test_find_min_with_floats():
    root = build_tree([1.5, 0.25, 3.7, -0.1])
    assert find_min(root) == -0.1


def test_find_min_duplicates_ignored():
    root = build_tree([5, 5, 5, 3, 3, 7])
    assert find_min(root) == 3


def test_find_min_empty_tree_raises():
    with pytest.raises(ValueError, match="tree is empty"):
        find_min(None)
