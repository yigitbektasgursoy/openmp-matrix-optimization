#!/usr/bin/env bash
#
# Usage:
#   ./run_vtune_analyses.sh
#
# Description:
#   Runs three VTune analyses (hotspots, memory-access, threading)
#   on four executables (matmul_naive, matmul_unrolled, matmul_blocked, matmul_aligned)
#   with various thread counts, and stores each run in a separate result directory.
#
#   Each is openable in VTune.

# ----------------------------
# Configuration
# ----------------------------
MATRIX_SIZE=2048
BLOCK_SIZE=64
THREADS_LIST=(2 4 8 16)

# Paths (modify these as needed)
LOG_DIR="../logs/vtune_logs"
BIN_DIR="../bin"
RESULT_DIR_BASE="../vtune_results"

# Create directories if they don't exist
mkdir -p "${LOG_DIR}"
mkdir -p "${RESULT_DIR_BASE}"

# Define each code and its necessary arguments (besides threads)
declare -A CODES
CODES["matmul_naive"]="${MATRIX_SIZE}"
CODES["matmul_unrolled"]="${MATRIX_SIZE}"
CODES["matmul_blocked"]="${MATRIX_SIZE} ${BLOCK_SIZE}"
CODES["matmul_aligned"]="${MATRIX_SIZE}"

# Analyses to run
ANALYSES=("hotspots" "memory-consumption" "threading")

# ----------------------------
# Main Loop
# ----------------------------
for code_name in "${!CODES[@]}"; do

    code_args="${CODES[$code_name]}"

    # Check executable presence
    if [ ! -x "${BIN_DIR}/${code_name}" ]; then
        echo "WARNING: '${BIN_DIR}/${code_name}' not found or not executable." | tee -a "${LOG_DIR}/errors.log"
        continue
    fi

    # For each thread count
    for T in "${THREADS_LIST[@]}"; do

        # For each analysis
        for analysis_type in "${ANALYSES[@]}"; do

            # Directory name for each run, e.g. matmul_naive_hotspots_threads_2
            RESULT_DIR="${RESULT_DIR_BASE}/${code_name}_${analysis_type}_threads_${T}"
            mkdir -p "${RESULT_DIR}"

            LOG_FILE="${LOG_DIR}/${code_name}_${analysis_type}_threads_${T}.log"

            echo "-----------------------------------------------------" | tee -a "${LOG_FILE}"
            echo " VTune ${analysis_type} Analysis:" | tee -a "${LOG_FILE}"
            echo "   Code:       ${code_name}" | tee -a "${LOG_FILE}"
            echo "   Args:       ${code_args}" | tee -a "${LOG_FILE}"
            echo "   Threads:    ${T}" | tee -a "${LOG_FILE}"
            echo "   Result Dir: ${RESULT_DIR}" | tee -a "${LOG_FILE}"
            echo "-----------------------------------------------------" | tee -a "${LOG_FILE}"

            OMP_NUM_THREADS="${T}" vtune \
                -collect "${analysis_type}" \
                -result-dir "${RESULT_DIR}" \
                -- "${BIN_DIR}/${code_name}" ${code_args} "${T}" >> "${LOG_FILE}" 2>&1

            if [ $? -eq 0 ]; then
                echo "Analysis completed successfully." | tee -a "${LOG_FILE}"
            else
                echo "Analysis failed. Check logs for details." | tee -a "${LOG_FILE}"
            fi
            echo | tee -a "${LOG_FILE}"
        done
    done
done

echo "All analyses completed. Logs stored in ${LOG_DIR}."
