import pytest

from tree import build_tree, insert
from task_02 import tree_sum


def test_tree_sum_empty_tree_is_zero():
    assert tree_sum(None) == 0


def test_tree_sum_single_node():
    root = insert(None, 42)
    assert tree_sum(root) == 42


def test_tree_sum_multiple_values():
    values = [20, 4, 26, 3, 9, 15, 30, 2]
    root = build_tree(values)
    assert tree_sum(root) == sum(values)


def test_tree_sum_with_negatives():
    values = [0, -5, 10, -100, 7]
    root = build_tree(values)
    assert tree_sum(root) == sum(values)


def test_tree_sum_with_floats():
    values = [1.5, 0.25, 3.7, -0.1]
    root = build_tree(values)
    assert tree_sum(root) == pytest.approx(sum(values))


def test_tree_sum_treats_tree_as_set():
    # set-semantics: duplicate inserts are dropped → sum reflects only distinct keys.
    root = build_tree([5, 5, 5, 3, 3, 7])
    assert tree_sum(root) == 5 + 3 + 7  # not 5+5+5+3+3+7
