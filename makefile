# ----------------------------------------------------------
#  Makefile for Four Parallel Matrix Multiplication Programs
#  Outputs executables in a ../bin folder
# ----------------------------------------------------------

# Compiler and flags
CC      = gcc
CFLAGS  = -fopenmp -O3 -Wall -Wextra
# (Add more flags if needed, e.g. -g, -march=native, etc.)

# Directories
SRC_DIR = ./src
BIN_DIR = ./bin

# Executable names (stored in bin/)
BIN_NAIVE    = $(BIN_DIR)/matmul_naive
BIN_UNROLLED = $(BIN_DIR)/matmul_unrolled
BIN_BLOCKED  = $(BIN_DIR)/matmul_blocked
BIN_ALIGNED  = $(BIN_DIR)/matmul_aligned
BIN_TEST     = $(BIN_DIR)/test_matmul

# Source files
SRC_NAIVE    = $(SRC_DIR)/matmul_naive.c
SRC_UNROLLED = $(SRC_DIR)/matmul_unrolled.c
SRC_BLOCKED  = $(SRC_DIR)/matmul_blocked.c
SRC_ALIGNED  = $(SRC_DIR)/matmul_aligned.c
SRC_TEST     = $(SRC_DIR)/test_matmul.c

# Ensure bin directory exists before building
MKDIR_P = mkdir -p

# Default rule: build all executables (including test_matmul)
all: $(BIN_NAIVE) $(BIN_UNROLLED) $(BIN_BLOCKED) $(BIN_ALIGNED) $(BIN_TEST)

# Build rules
$(BIN_NAIVE): $(SRC_NAIVE)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_UNROLLED): $(SRC_UNROLLED)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_BLOCKED): $(SRC_BLOCKED)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_ALIGNED): $(SRC_ALIGNED)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

# If test_matmul.c contains all 4 matmul functions within the same file,
# it only depends on SRC_TEST. If it requires linking multiple .o files,
# you'd adjust accordingly.
$(BIN_TEST): $(SRC_TEST)
	@$(MKDIR_P) $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

# Clean rule: removes the compiled executables
# (but does not delete the bin folder itself)
clean:
	rm -f $(BIN_DIR)/*.exe

# --------------------------------------------------------------------
# Optional convenience commands to run each executable:
#   Usage: make run_naive N=1024 T=8
# --------------------------------------------------------------------
run_naive: $(BIN_NAIVE)
	@$(BIN_NAIVE) $(N) $(T)

run_unrolled: $(BIN_UNROLLED)
	@$(BIN_UNROLLED) $(N) $(T)

# For blocked, we also need a block size B, e.g. make run_blocked N=1024 T=8 B=64
run_blocked: $(BIN_BLOCKED)
	@$(BIN_BLOCKED) $(N) $(T) $(B)

run_aligned: $(BIN_ALIGNED)
	@$(BIN_ALIGNED) $(N) $(T)

# --------------------------------------------------------------------
# Run the test executable (test_matmul)
# This typically does a small 5x5 check comparing all methods.
# --------------------------------------------------------------------
run_test: $(BIN_TEST)
	@$(BIN_TEST)
