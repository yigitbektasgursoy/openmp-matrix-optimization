# ----------------------------------------------------------
#  Makefile for Sequential and Parallel Matrix Multiplication
# ----------------------------------------------------------

# Compiler and flags
CC      = gcc
CFLAGS  = -fopenmp -O3 -Wall -Wextra

# Directories
SRC_DIR = ./src
BIN_DIR = ./bin

# Sequential executables
BIN_NAIVE_SEQ    = $(BIN_DIR)/matmul_naive_seq
BIN_UNROLLED_SEQ = $(BIN_DIR)/matmul_unrolled_seq
BIN_BLOCKED_SEQ  = $(BIN_DIR)/matmul_blocked_seq
BIN_ALIGNED_SEQ  = $(BIN_DIR)/matmul_aligned_seq

# Parallel executables
BIN_NAIVE_PARALLEL    = $(BIN_DIR)/matmul_naive_parallel
BIN_UNROLLED_PARALLEL = $(BIN_DIR)/matmul_unrolled_parallel
BIN_BLOCKED_PARALLEL  = $(BIN_DIR)/matmul_blocked_parallel
BIN_ALIGNED_PARALLEL  = $(BIN_DIR)/matmul_aligned_parallel

# Test executable
BIN_TEST = $(BIN_DIR)/test_matmul

# Source files - Sequential
SRC_NAIVE_SEQ    = $(SRC_DIR)/matmul_naive_seq.c
SRC_UNROLLED_SEQ = $(SRC_DIR)/matmul_unrolled_seq.c
SRC_BLOCKED_SEQ  = $(SRC_DIR)/matmul_blocked_seq.c
SRC_ALIGNED_SEQ  = $(SRC_DIR)/matmul_aligned_seq.c

# Source files - Parallel
SRC_NAIVE_PARALLEL    = $(SRC_DIR)/matmul_naive_parallel.c
SRC_UNROLLED_PARALLEL = $(SRC_DIR)/matmul_unrolled_parallel.c
SRC_BLOCKED_PARALLEL  = $(SRC_DIR)/matmul_blocked_parallel.c
SRC_ALIGNED_PARALLEL  = $(SRC_DIR)/matmul_aligned_parallel.c

# Test source
SRC_TEST = $(SRC_DIR)/test_matmul.c

# Directory creation
MKDIR_P = mkdir -p

# Default target: build everything
all: $(BIN_NAIVE_SEQ) $(BIN_UNROLLED_SEQ) $(BIN_BLOCKED_SEQ) $(BIN_ALIGNED_SEQ) \
     $(BIN_NAIVE_PARALLEL) $(BIN_UNROLLED_PARALLEL) $(BIN_BLOCKED_PARALLEL) $(BIN_ALIGNED_PARALLEL) \
     $(BIN_TEST)

# Build rules - Sequential
$(BIN_NAIVE_SEQ): $(SRC_NAIVE_SEQ)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_UNROLLED_SEQ): $(SRC_UNROLLED_SEQ)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_BLOCKED_SEQ): $(SRC_BLOCKED_SEQ)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_ALIGNED_SEQ): $(SRC_ALIGNED_SEQ)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

# Build rules - Parallel
$(BIN_NAIVE_PARALLEL): $(SRC_NAIVE_PARALLEL)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_UNROLLED_PARALLEL): $(SRC_UNROLLED_PARALLEL)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_BLOCKED_PARALLEL): $(SRC_BLOCKED_PARALLEL)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_ALIGNED_PARALLEL): $(SRC_ALIGNED_PARALLEL)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

# Test build rule
$(BIN_TEST): $(SRC_TEST)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

# Clean rule
clean:
	rm -f $(BIN_DIR)/*

# Run targets - Sequential
run_naive_seq: $(BIN_NAIVE_SEQ)
	@$(BIN_NAIVE_SEQ) $(N) $(T)

run_unrolled_seq: $(BIN_UNROLLED_SEQ)
	@$(BIN_UNROLLED_SEQ) $(N) $(T)

run_blocked_seq: $(BIN_BLOCKED_SEQ)
	@$(BIN_BLOCKED_SEQ) $(N) $(T) $(B)

run_aligned_seq: $(BIN_ALIGNED_SEQ)
	@$(BIN_ALIGNED_SEQ) $(N) $(T)

# Run targets - Parallel
run_naive_parallel: $(BIN_NAIVE_PARALLEL)
	@$(BIN_NAIVE_PARALLEL) $(N) $(T)

run_unrolled_parallel: $(BIN_UNROLLED_PARALLEL)
	@$(BIN_UNROLLED_PARALLEL) $(N) $(T)

run_blocked_parallel: $(BIN_BLOCKED_PARALLEL)
	@$(BIN_BLOCKED_PARALLEL) $(N) $(T) $(B)

run_aligned_parallel: $(BIN_ALIGNED_PARALLEL)
	@$(BIN_ALIGNED_PARALLEL) $(N) $(T)

# Test run target
run_test: $(BIN_TEST)
	@$(BIN_TEST)

# Declare phony targets
.PHONY: all clean run_naive_seq run_unrolled_seq run_blocked_seq run_aligned_seq \
        run_naive_parallel run_unrolled_parallel run_blocked_parallel run_aligned_parallel run_test
