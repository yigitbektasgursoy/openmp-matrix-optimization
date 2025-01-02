#!/usr/bin/env bash

# Define thread counts
THREADS=(1 2 4 8 16)

# Program configuration
MATRIX_SIZE=2048
BLOCK_SIZE=64
PROGRAMS=("../bin/matmul_naive" "../bin/matmul_unrolled" "../bin/matmul_blocked" "../bin/matmul_aligned")
PROGRAM_NAMES=("Naive" "Unrolled" "Blocked" "Aligned")

# Output directory for logs
LOG_DIR="../logs/cache_hit_miss_logs"
mkdir -p "${LOG_DIR}"

# Loop through each program
for i in "${!PROGRAMS[@]}"; do
    PROGRAM="${PROGRAMS[$i]}"
    PROGRAM_NAME="${PROGRAM_NAMES[$i]}"

    # Ensure the program exists
    if [ ! -x "${PROGRAM}" ]; then
        echo "Error: Program '${PROGRAM}' not found or not executable."
        continue
    fi

    # Combined log file for the program
    LOG_FILE="${LOG_DIR}/${PROGRAM_NAME}_cache_misses.log"
    echo "" > "${LOG_FILE}"  # Clear or create the log file

    # Loop through each thread count
    for T in "${THREADS[@]}"; do
        echo "Running ${PROGRAM_NAME} with ${T} threads..." | tee -a "${LOG_FILE}"

        # Run perf with the specified thread count and append the results to the program-specific log file
        perf stat -e L1-dcache-load-misses,L1-dcache-loads,LLC-load-misses,LLC-loads \
            ${PROGRAM} ${MATRIX_SIZE} ${T} ${BLOCK_SIZE} >> "${LOG_FILE}" 2>&1

        echo "Results for ${T} threads saved to ${LOG_FILE}" | tee -a "${LOG_FILE}"
    done

done

echo "All measurements completed. Logs stored in ${LOG_DIR}."
