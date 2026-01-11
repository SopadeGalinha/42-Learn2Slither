# Learn2Slither - C Test Suite

Comprehensive test suite for the C game engine.

## Layout

```
c_src/tests/
├── tests.h                      # Macros and shared interfaces
├── test_board_creation.c        # Creation/destruction (5 funcs)
├── test_board_edge_cases.c      # Edge cases (5 funcs)
├── test_board_validation.c      # Validation (5 funcs)
├── test_board_memory.c          # Memory/stress (5 funcs)
├── test_runner.c                # Main coordinator (1 func)
└── Makefile                     # Test build
```

## Running Tests

`make test` already runs Valgrind by default.

```bash
cd c_src/tests && make test
```

## Cleaning

```bash
cd c_src/tests && make clean   # Remove objects
cd c_src/tests && make fclean  # Remove executable
```

## Test Coverage

### Test: Board Creation (4 tests)
- ✅ Create board size 10
- ✅ Destroy board cleanly
- ✅ Create with max size 20
- ✅ Create with min size 8

### Test: Edge Cases (4 tests)
- ✅ Too small (< 8) → defaults to 10
- ✅ Too large (> 20) → defaults to 10
- ✅ Negative size → defaults to 10
- ✅ Zero size → defaults to 10

### Test: Board Validation (4 tests)
- ✅ Snake initialized correctly
- ✅ Apple counts correct (2 green, 1 red for size 10)
- ✅ Board reset works
- ✅ Game not over initially

### Test: Memory & Stress (4 tests)
- ✅ Multiple create/destroy (100 iterations) → no leaks
- ✅ Destroy NULL board is safe
- ✅ Allocate multiple sizes
- ✅ State consistency

## 42 Norminette Compliance

✅ Max 5 functions per file
✅ Max 25 lines per function
✅ Max 4 variables per function
✅ 42 headers on all files
✅ No warnings (-Wall -Wextra -Werror)

## Valgrind Result

```
==14680== HEAP SUMMARY:
==14680==     in use at exit: 0 bytes in 0 blocks
==14680==   total heap usage: 2,767 allocs, 2,767 frees
==14680==
==14680== All heap blocks were freed -- no leaks are possible
==14680== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

✅ **No memory leaks**
✅ **No segmentation faults**
✅ **All 16 tests pass**

## Test Macros

```c
// Simple assertion
ASSERT(condition, "error message")

// Equality assertion
ASSERT_EQ(actual, expected, "message")

// Run a test (increments counters automatically)
RUN_TEST("test name", test_function)
```

## How to Add a New Test

1. Create `static bool test_something(void)`
2. Use `ASSERT` or `ASSERT_EQ` for checks
3. Add it to the `t_test_result` struct in the runner
4. Call `RUN_TEST("name", test_something)` in the runner

Example:
```c
static bool test_example(void)
{
    Board *board = board_create(10);
    ASSERT(board != NULL, "Allocation failed");
    ASSERT_EQ(board->size, 10, "Wrong size");
    board_destroy(board);
    return (true);
}
```
