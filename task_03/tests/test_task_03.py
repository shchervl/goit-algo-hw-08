import pytest

from task_03 import min_merge_cost, naive_merge_cost


def test_empty_input_is_zero():
    assert min_merge_cost([]) == 0


def test_single_cable_needs_no_merge():
    assert min_merge_cost([7]) == 0


def test_two_cables_just_sum():
    assert min_merge_cost([4, 6]) == 10


def test_known_answer_one_to_five():
    # 1+2=3, 3+3=6, 4+5=9, 6+9=15 → 3+6+9+15 = 33
    assert min_merge_cost([1, 2, 3, 4, 5]) == 33


def test_order_does_not_affect_result():
    a = min_merge_cost([1, 2, 3, 4, 5])
    b = min_merge_cost([5, 4, 3, 2, 1])
    c = min_merge_cost([3, 1, 4, 5, 2])
    assert a == b == c


def test_greedy_beats_naive_left_to_right():
    # Naive left-to-right: ((1+8)+9)+10 → 9+18+28 = 55
    # Greedy:              (1+8)+(9+10) → 9+19+28 → wait, let's compute carefully.
    # cables = [1, 8, 9, 10]
    # heap: pop 1, 8 → cost 9, total 9, push 9 → [9, 9, 10]
    # heap: pop 9, 9 → cost 18, total 27, push 18 → [10, 18]
    # heap: pop 10, 18 → cost 28, total 55
    # Hmm same. Use a more skewed example:
    # [1, 2, 100]:
    #   greedy: 1+2=3, then 3+100=103 → total 106
    #   naive (any order with 100 first): 1+100=101, 2+101=103 → total 204
    assert min_merge_cost([1, 2, 100]) == 106


def test_floats_are_supported():
    assert min_merge_cost([1.5, 2.5, 4.0]) == pytest.approx(12.0)


def test_duplicates_are_allowed():
    # Duplicate-length cables are real (multiset, unlike the AVL set).
    # [4, 4, 4, 4]: pop 4,4=8 (total 8), pop 4,4=8 (total 16), pop 8,8=16 (total 32)
    assert min_merge_cost([4, 4, 4, 4]) == 32


def test_non_numeric_raises():
    with pytest.raises(TypeError):
        min_merge_cost([1, 2, "x"])


def test_bool_raises():
    with pytest.raises(TypeError):
        min_merge_cost([1, 2, True])


def test_zero_length_raises():
    with pytest.raises(ValueError):
        min_merge_cost([1, 0, 3])


def test_negative_length_raises():
    with pytest.raises(ValueError):
        min_merge_cost([1, -2, 3])


def test_naive_merge_known_answer():
    # [1, 2, 100]: (1+2)=3, (3+100)=103 → total 106
    # naive left→right: (1+2)=3, then (3+100)=103 → total 106 (same here!)
    # Use [1, 100, 2]: (1+100)=101, then (101+2)=103 → total 204
    assert naive_merge_cost([1, 100, 2]) == 204


def test_naive_merge_two_cables_matches_greedy():
    assert naive_merge_cost([4, 6]) == min_merge_cost([4, 6]) == 10


def test_naive_merge_empty_or_single_is_zero():
    assert naive_merge_cost([]) == 0
    assert naive_merge_cost([42]) == 0


def test_greedy_is_never_worse_than_naive():
    cases = [
        [1, 2, 3, 4, 5],
        [1, 100, 2, 99, 3],
        [10, 20, 30, 40, 50, 60],
        [1, 1, 1, 1, 1, 1],
    ]
    for cables in cases:
        assert min_merge_cost(cables) <= naive_merge_cost(cables)
