"""Task 03b: external-merge-sort framing of Task 03.

Same algorithm as Task 03, but applied to **real** sorted files on disk.
"""

import heapq
import logging
import sys
import tempfile
import time
from pathlib import Path

RESOURCES = Path(__file__).parent / "resources"

log = logging.getLogger(__name__)


def _bytes_formatter(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def read_files(directory: Path) -> list[Path]:
    """Return sorted list of `file_*.txt` present in `directory`.

    Returns an empty list if the directory is missing or has no matches.
    The committed `resources/` directory is the canonical input set.
    """
    if not directory.exists():
        return []
    return sorted(directory.glob("file_*.txt"))


def _merge_files_content(path_a: Path, path_b: Path, out_path: Path) -> int:
    """Merge two sorted files into `out_path`. Returns bytes written.

    `key=int` is required because the files contain numeric data but
    `heapq.merge` would otherwise compare lines as strings (so e.g.
    "100" would land before "9").
    """
    bytes_written = 0
    with path_a.open() as fa, path_b.open() as fb, out_path.open("w") as fo:
        for line in heapq.merge(fa, fb, key=int):
            fo.write(line)
            bytes_written += len(line)
    return bytes_written


def huffman_merge(file_paths: list[Path], work_dir: Path) -> tuple[Path, int]:
    """Optimal Merge Pattern (Huffman 1952): always merge the two smallest first.

    Uses a min-heap keyed by file size. Returns (final_path, total_bytes_written).
    Each byte ends up being copied ~log N times instead of ~N times in the
    sequential strategy.

    Raises ValueError on empty input. With a single input file the function
    short-circuits: it returns that input path unchanged and never touches
    `work_dir`.
    """
    if not file_paths:
        raise ValueError("file_paths must contain at least one file")
    if len(file_paths) == 1:
        return file_paths[0], 0
    work_dir.mkdir(parents=True, exist_ok=True)
    n_merges = len(file_paths) - 1
    log.info("huffman:    starting %d merges of %d files", n_merges, len(file_paths))
    t0 = time.perf_counter()
    # Heap entries are (size, counter, path); counter breaks ties so Paths are never compared.
    heap = [(p.stat().st_size, i, p) for i, p in enumerate(file_paths)]
    heapq.heapify(heap)
    counter = len(heap)
    total_bytes = 0
    width = len(str(n_merges))
    for step in range(1, n_merges + 1):
        sa, _, pa = heapq.heappop(heap)
        sb, _, pb = heapq.heappop(heap)
        out = work_dir / f"merge_{counter:03d}.txt"
        counter += 1
        bw = _merge_files_content(pa, pb, out)
        total_bytes += bw
        heapq.heappush(heap, (out.stat().st_size, counter, out))
        log.debug(
            "huffman:    step %0*d/%d  %s ← %s + %s  (heap: %d left)",
            width,
            step,
            n_merges,
            _bytes_formatter(bw),
            _bytes_formatter(sa),
            _bytes_formatter(sb),
            len(heap),
        )
    log.info(
        "huffman:    done in %.2fs, %s processed",
        time.perf_counter() - t0,
        _bytes_formatter(total_bytes),
    )
    return heap[0][2], total_bytes


def sequential_merge(file_paths: list[Path], work_dir: Path) -> tuple[Path, int]:
    """Merge files in input order, accumulating into a running file.

    Returns (final_path, total_bytes_written). The running file gets re-read
    on every step, so each byte is copied ~N times — quadratic in total work.

    Raises ValueError on empty input. With a single input file the function
    short-circuits: it returns that input path unchanged and never touches
    `work_dir`.
    """
    if not file_paths:
        raise ValueError("file_paths must contain at least one file")
    if len(file_paths) == 1:
        return file_paths[0], 0
    work_dir.mkdir(parents=True, exist_ok=True)
    n_merges = len(file_paths) - 1
    log.info("sequential: starting %d merges of %d files", n_merges, len(file_paths))
    t0 = time.perf_counter()
    running = file_paths[0]
    total_bytes = 0
    for i, p in enumerate(file_paths[1:], start=1):
        out = work_dir / f"seq_{i:03d}.txt"
        bw = _merge_files_content(running, p, out)
        total_bytes += bw
        running = out
    log.info(
        "sequential: done in %.2fs, %s processed",
        time.perf_counter() - t0,
        _bytes_formatter(total_bytes),
    )
    return running, total_bytes


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        datefmt="%H:%M:%S",
    )

    paths = read_files(RESOURCES)
    if not paths:
        log.error("no input files found in %s — nothing to do", RESOURCES)
        sys.exit(1)

    total = sum(p.stat().st_size for p in paths)
    log.info(
        "read:     %d files from %s (%s total)",
        len(paths),
        RESOURCES,
        _bytes_formatter(total),
    )
    sizes = [p.stat().st_size for p in paths]
    log.info(
        "input:    size range %s – %s",
        _bytes_formatter(min(sizes)),
        _bytes_formatter(max(sizes)),
    )

    # Warm-up: read every input byte once so both strategies face an
    # equally hot OS file cache. The bytes are discarded — only the
    # cache state matters.
    log.info("warmup:   pre-reading %d input files into OS cache", len(paths))
    t_warmup = time.perf_counter()
    warmed_bytes = sum(len(p.read_bytes()) for p in paths)
    log.info(
        "warmup:   done in %.2fs, %s read (discarded)",
        time.perf_counter() - t_warmup,
        _bytes_formatter(warmed_bytes),
    )

    # Intermediate merge outputs go into a temp dir that is wiped on exit.
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        t0 = time.perf_counter()
        _, sequential_bytes = sequential_merge(paths, tmp_path / "sequential")
        t_sequential = time.perf_counter() - t0

        t0 = time.perf_counter()
        _, huffman_bytes = huffman_merge(paths, tmp_path / "huffman")
        t_huffman = time.perf_counter() - t0

    bar = "═" * 72
    log.info(
        "benchmark report:\n"
        "%s\n"
        "%-12s%-20s%-14s%s\n"
        "%-12s%-20s%-14s%s\n"
        "%-12s%-20s%-14s%s\n"
        "\n"
        "(N = total input bytes, K = number of input files)\n"
        "\n"
        "Huffman moves %.1f%% fewer bytes and runs %.2fx faster than sequential.\n"
        "The gap widens as K grows — the ratio scales as K / log K, so doubling\n"
        "the file count more than doubles the advantage.\n"
        "%s",
        bar,
        "Strategy",
        "Bytes processed",
        "Wall time",
        "Big-O",
        "huffman",
        _bytes_formatter(huffman_bytes),
        f"{t_huffman * 1000:.1f} ms",
        "O(N log K)",
        "sequential",
        _bytes_formatter(sequential_bytes),
        f"{t_sequential * 1000:.1f} ms",
        "O(N · K)",
        100 * (sequential_bytes - huffman_bytes) / sequential_bytes,
        t_sequential / t_huffman,
        bar,
    )
