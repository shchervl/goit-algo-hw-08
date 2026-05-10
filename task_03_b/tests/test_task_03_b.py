from pathlib import Path

import pytest

from task_03_b import huffman_merge, read_files, sequential_merge


@pytest.fixture
def small_files(tmp_path):
    """Four small sorted files of varied sizes — disjoint ranges so the merged
    output is also strictly sorted and easy to verify."""
    src = tmp_path / "src"
    src.mkdir()
    contents = [
        [10, 20],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [11, 12, 13],
        [9, 14, 15, 16, 17],
    ]
    paths = []
    for i, items in enumerate(contents):
        path = src / f"file_{i:02d}.txt"
        path.write_text("".join(f"{x}\n" for x in items))
        paths.append(path)
    return paths


def _read_lines(path: Path) -> list[str]:
    return path.read_text().splitlines()


def test_read_files_returns_empty_for_missing_directory(tmp_path):
    assert read_files(tmp_path / "does_not_exist") == []


def test_read_files_picks_up_committed_files(small_files):
    src = small_files[0].parent
    assert read_files(src) == small_files


def test_huffman_output_is_sorted(small_files, tmp_path):
    out, _ = huffman_merge(small_files, tmp_path / "work")
    nums = [int(x) for x in _read_lines(out)]
    assert nums == sorted(nums)


def test_sequential_output_is_sorted(small_files, tmp_path):
    out, _ = sequential_merge(small_files, tmp_path / "work")
    nums = [int(x) for x in _read_lines(out)]
    assert nums == sorted(nums)


def test_both_strategies_produce_same_content(small_files, tmp_path):
    h_out, _ = huffman_merge(small_files, tmp_path / "h")
    s_out, _ = sequential_merge(small_files, tmp_path / "s")
    assert h_out.read_text() == s_out.read_text()


def test_huffman_moves_no_more_bytes_than_sequential(small_files, tmp_path):
    _, h_bytes = huffman_merge(small_files, tmp_path / "h")
    _, s_bytes = sequential_merge(small_files, tmp_path / "s")
    assert h_bytes <= s_bytes


def test_huffman_merge_raises_on_empty_input(tmp_path):
    with pytest.raises(ValueError, match="at least one file"):
        huffman_merge([], tmp_path / "work")


def test_sequential_merge_raises_on_empty_input(tmp_path):
    with pytest.raises(ValueError, match="at least one file"):
        sequential_merge([], tmp_path / "work")


def test_single_file_short_circuits_without_touching_work_dir(small_files, tmp_path):
    only = [small_files[0]]
    h_work = tmp_path / "h"
    s_work = tmp_path / "s"

    h_out, h_bytes = huffman_merge(only, h_work)
    s_out, s_bytes = sequential_merge(only, s_work)

    assert h_out == only[0] and h_bytes == 0
    assert s_out == only[0] and s_bytes == 0
    assert not h_work.exists()
    assert not s_work.exists()
