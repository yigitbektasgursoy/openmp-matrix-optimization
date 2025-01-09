#!/usr/bin/env bash

# =============================================================================
# VTune Performance Analysis Automation Script
# =============================================================================
#
# Description:
#   Automates the execution of multiple VTune analyses (hotspots, memory-consumption, threading)
#   on various matrix multiplication executables with different configurations.
#   For parallel versions: tests different thread counts
#   For sequential versions: single execution without thread variations
#
# Usage:
#   ./run_vtune_analyses.sh
#
# Requirements:
#   - Intel VTune Profiler installed and accessible via the command line.
#   - Executables placed in the specified BIN_DIR.
#
# =============================================================================

# ----------------------------
# Configuration
# ----------------------------

# Matrix configurations
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

# VTune analyses to perform
ANALYSES="threading"

# Directories
LOG_DIR="../logs/vtune_logs"
BIN_DIR="../bin"
RESULT_DIR_BASE="../vtune_results"

# ----------------------------
# Setup Environment
# ----------------------------

# Clear previous VTune results
echo "Clearing previous VTune results in ${RESULT_DIR_BASE}..."
rm -rf "${RESULT_DIR_BASE}"
mkdir -p "${LOG_DIR}"
mkdir -p "${RESULT_DIR_BASE}"
echo "Setup complete."

# ----------------------------
# Helper Functions
# ----------------------------

# Function to log messages with timestamps
log_message() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') : ${message}"
}

# Function to perform VTune analysis
perform_analysis() {
    local program="$1"
    local matrix_size="$2"
    local threads="$3"
    local analysis_type="$4"

    # Construct argument list based on program type
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

    # Define result directory (include thread info only for parallel versions)
    if [[ "$program" == *"parallel"* ]]; then
        RESULT_DIR="${RESULT_DIR_BASE}/${program}_N${matrix_size}_T${threads}_${analysis_type}"
        LOG_FILE="${LOG_DIR}/${program}_N${matrix_size}_T${threads}_${analysis_type}.log"
    else
        RESULT_DIR="${RESULT_DIR_BASE}/${program}_N${matrix_size}_${analysis_type}"
        LOG_FILE="${LOG_DIR}/${program}_N${matrix_size}_${analysis_type}.log"
    fi
    mkdir -p "${RESULT_DIR}"

    # Log the start of analysis
    if [[ "$program" == *"parallel"* ]]; then
        log_message "Starting ${analysis_type} analysis for ${program} (N=${matrix_size}, T=${threads})" | tee -a "${LOG_FILE}"
    else
        log_message "Starting ${analysis_type} analysis for ${program} (N=${matrix_size})" | tee -a "${LOG_FILE}"
    fi

    # Set environment variable for thread count only for parallel versions
    if [[ "$program" == *"parallel"* ]]; then
        export OMP_NUM_THREADS="${threads}"
    else
        unset OMP_NUM_THREADS
    fi

    # Execute VTune analysis
    vtune -collect "${analysis_type}" \
          -result-dir "${RESULT_DIR}" \
          -- "${BIN_DIR}/${program}" ${args} >> "${LOG_FILE}" 2>&1

    # Check for success
    if [ $? -eq 0 ]; then
        log_message "Completed ${analysis_type} analysis successfully." | tee -a "${LOG_FILE}"
    else
        log_message "ERROR: ${analysis_type} analysis failed. Check ${LOG_FILE} for details." | tee -a "${LOG_FILE}"
    fi

    echo "" >> "${LOG_FILE}"
}

# ----------------------------
# Main Execution Loop
# ----------------------------

log_message "Starting VTune performance analyses..."

for matrix_size in "${MATRIX_SIZES[@]}"; do
    for program in "${PROGRAMS[@]}"; do
        # Check if the executable exists and is executable
        if [ ! -x "${BIN_DIR}/${program}" ]; then
            log_message "WARNING: Executable '${BIN_DIR}/${program}' not found or not executable." | tee -a "${LOG_DIR}/errors.log"
            continue
        fi

        # For parallel versions: run with different thread counts
        # For sequential versions: run once without thread variations
        if [[ "$program" == *"parallel"* ]]; then
            for threads in "${THREADS_LIST[@]}"; do
                for analysis in "${ANALYSES[@]}"; do
                    perform_analysis "$program" "$matrix_size" "$threads" "$analysis"
                done
            done
        else
            # Sequential version - run once without thread count
            for analysis in "${ANALYSES[@]}"; do
                perform_analysis "$program" "$matrix_size" "" "$analysis"
            done
        fi
    done
done

log_message "All VTune analyses completed. Logs are available in ${LOG_DIR}."
