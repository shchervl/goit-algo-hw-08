# goit-algo-hw-08

Homework 08 — tree and heap algorithms.

## Tasks

- **Task 01** (`task_01/task_01.py`) — find the smallest value in an AVL tree.
- **Task 02** (`task_02/task_02.py`) — find the sum of all values in an AVL tree.
- **Task 03** (`task_03/task_03.py`) — minimum total cost of merging cables (Huffman-style greedy with a min-heap).
- **Task 03b** (`task_03_b/task_03_b.py`) — same algorithm applied to real sorted files on disk; benchmarks Huffman (heap-based optimal) vs sequential merge in actual bytes processed and wall time.

## Tree implementation

The shared AVL tree lives in `tree/avl_tree.py`. It is a **classical
BST/AVL that models a mathematical set**: each value is stored at most
once. Re-inserting an existing key is a silent no-op.

This means functions like `tree_sum` operate on the **distinct** keys
present in the tree, not on the original input list. The Task 02 demo
makes this visible by printing both the original (possibly duplicate)
input and the in-order contents of the tree.

If multiset/bag semantics are ever needed, extend `AVLNode` with a
`count` field rather than storing duplicate nodes.

## Project layout

```
goit-algo-hw-08/
├── tree/                       # shared AVL tree + its own tests
│   ├── avl_tree.py
│   └── tests/test_avl_tree.py
├── task_01/
│   ├── task_01.py              # find_min + demo
│   └── tests/test_task_01.py
├── task_02/
│   ├── task_02.py              # tree_sum + demo
│   └── tests/test_task_02.py
├── task_03/
│   ├── task_03.py              # min_merge_cost + demo
│   └── tests/test_task_03.py
└── task_03_b/
    ├── task_03_b.py            # external-merge benchmark on real files
    ├── resources/              # example files
    └── tests/test_task_03_b.py
```

## Setup

Requires Python ≥ 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync                         # install deps (creates .venv)
```

## Running the tasks

```bash
uv run python -m task_01.task_01
uv run python -m task_02.task_02
uv run python -m task_03.task_03
uv run python -m task_03_b.task_03_b    # simple benchmarks based on file merge examples
```

Each script builds a random AVL tree and prints the result of the task
function.

## Running tests

```bash
uv run pytest                   # all tests in the repo
uv run pytest tree/             # only tree-implementation tests
uv run pytest task_01/          # only Task 01 tests
uv run pytest task_02/          # only Task 02 tests
uv run pytest task_03/          # only Task 03 tests
uv run pytest task_03_b/        # only Task 03b tests
uv run pytest -v                # verbose, one line per test
```
