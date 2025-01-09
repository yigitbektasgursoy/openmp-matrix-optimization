#!/usr/bin/env bash

# =============================================================================
# Cache Performance Analysis Script
# =============================================================================
#
# Description:
#   Measures cache performance metrics (L1 and LLC misses/loads) for different
#   matrix multiplication implementations (parallel and sequential) using Linux perf.
#
# Usage:
#   ./measure_cache_perf.sh
#
# Requirements:
#   - Linux perf tools installed
#   - Matrix multiplication executables in ../bin directory
# =============================================================================

# ----------------------------
# Configuration
# ----------------------------

# Matrix sizes
MATRIX_SIZES=(1024 2048 4096)

# Thread configurations (only for parallel versions)
THREADS_LIST=(2 4 8 16)

# Programs to analyze
PROGRAMS=(
    "matmul_aligned_parallel"
    "matmul_aligned_seq"
    "matmul_blocked_parallel"
    "matmul_blocked_seq"
    "matmul_naive_parallel"
    "matmul_naive_seq"
    "matmul_unrolled_parallel"
    "matmul_unrolled_seq"
)

# Directories
BIN_DIR="../bin"
LOG_DIR="../logs/cache_hit_miss_logs"

# Create log directory
mkdir -p "${LOG_DIR}"

# ----------------------------
# Helper Functions
# ----------------------------

# Function to log messages with timestamps
log_message() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') : ${message}"
}

# Function to perform cache analysis
perform_cache_analysis() {
    local program="$1"
    local matrix_size="$2"
    local threads="$3"
    
    # Construct program path
    local program_path="${BIN_DIR}/${program}"
    
    # Construct arguments based on program type
    if [[ "$program" == *"blocked"* ]]; then
        # For blocked versions (matrix_size and block_size=64)
        args="${matrix_size} 64"
        # Add thread count only for parallel versions
        if [[ "$program" == *"parallel"* ]]; then
            args="${matrix_size} ${threads} 64"
        fi
    else
        # For non-blocked versions (just matrix_size)
        args="${matrix_size}"
        # Add thread count only for parallel versions
        if [[ "$program" == *"parallel"* ]]; then
            args="${matrix_size} ${threads}"
        fi
    fi
    
    # Create log file name
    if [[ "${program}" == *"parallel"* ]]; then
        log_file="${LOG_DIR}/${program}_N${matrix_size}_T${threads}.log"
    else
        log_file="${LOG_DIR}/${program}_N${matrix_size}.log"
    fi
    
    # Log header
    {
        echo "Cache Performance Analysis"
        echo "=========================="
        echo "Program: ${program}"
        echo "Matrix Size: ${matrix_size}"
        if [[ "${program}" == *"blocked"* ]]; then
            echo "Block Size: 64"
        fi
        if [[ "${program}" == *"parallel"* ]]; then
            echo "Threads: ${threads}"
        fi
        echo "Date: $(date)"
        echo "==========================\n"
    } > "${log_file}"
    
    # Set thread count for parallel versions
    if [[ "${program}" == *"parallel"* ]]; then
        export OMP_NUM_THREADS="${threads}"
    else
        unset OMP_NUM_THREADS
    fi
    
    # Run perf stat
    if [[ "${program}" == *"parallel"* ]]; then
        log_message "Running analysis for ${program} (N=${matrix_size}, T=${threads})"
    else
        log_message "Running analysis for ${program} (N=${matrix_size})"
    fi
    
    perf stat -e L1-dcache-load-misses,L1-dcache-loads,LLC-load-misses,LLC-loads \
        "${program_path}" ${args} 2>> "${log_file}"
    
    # Add separator
    echo -e "\n---------------------------\n" >> "${log_file}"
    
    log_message "Analysis completed. Results saved to ${log_file}"
}

# ----------------------------
# Main Execution
# ----------------------------

log_message "Starting cache performance analysis..."

for matrix_size in "${MATRIX_SIZES[@]}"; do
    for program in "${PROGRAMS[@]}"; do
        # Check if executable exists
        if [ ! -x "${BIN_DIR}/${program}" ]; then
            log_message "WARNING: Executable '${BIN_DIR}/${program}' not found or not executable."
            continue
        fi
        
        # Handle parallel vs sequential programs
        if [[ "${program}" == *"parallel"* ]]; then
            # For parallel programs, run with each thread count
            for threads in "${THREADS_LIST[@]}"; do
                perform_cache_analysis "${program}" "${matrix_size}" "${threads}"
            done
        else
            # For sequential programs, run once without thread count
            perform_cache_analysis "${program}" "${matrix_size}" ""
        fi
    done
done

log_message "All analyses completed. Results available in ${LOG_DIR}"
