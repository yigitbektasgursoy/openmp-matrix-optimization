# Matrix Multiplication Optimization Project

This project explores optimization techniques for matrix multiplication, a computationally intensive operation widely used in scientific computing, graphics, and machine learning. By leveraging techniques such as parallelization, loop unrolling, cache blocking, and memory alignment, the project demonstrates performance improvements on modern hardware using C and OpenMP.

---

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Optimization Techniques](#optimization-techniques)
4. [Compilation and Execution](#compilation-and-execution)
5. [Performance Analysis](#performance-analysis)
6. [Tools and Libraries Used](#tools-and-libraries-used)
7. [Results and Observations](#results-and-observations)
8. [Future Work](#future-work)

---

## **Project Overview**

Matrix multiplication is an essential operation that often serves as a performance benchmark. This project implements and compares the following methods for matrix multiplication:
- **Naive Implementation**: A straightforward triple-nested loop.
- **Loop Unrolling**: Reducing loop overhead by manually unrolling iterations.
- **Cache Blocking (Tiling)**: Improving cache locality by breaking matrices into blocks.
- **Memory Alignment**: Aligning data to reduce cache and memory access overheads.

The project evaluates these techniques by analyzing execution time, cache performance, and scalability across multiple threads.

---

## **Project Structure**

### **Directories**
- **`bin/`**: Contains compiled executable files for different implementations.
- **`graphs/`**: Performance visualizations, such as execution time, speedup, and cache miss rate charts.
- **`logs/`**: Stores performance logs, including cache miss rates and threading details.
- **`report/`**: Detailed project documentation and analysis in `.docx` and `.pdf` formats.
- **`scripts/`**: Python and shell scripts for automation, performance analysis, and visualization.
- **`src/`**: Source code files for the matrix multiplication implementations.
- **`vtune_results/`**: Intel VTune profiler results for detailed performance analysis.

### **Files**
#### Source Code (`src/`)
1. **`matmul_naive.c`**:  
   Implements the naive triple-nested loop approach.
   
2. **`matmul_unrolled.c`**:  
   Optimized version with loop unrolling for better performance.

3. **`matmul_blocked.c`**:  
   Implements cache blocking to enhance memory locality.

4. **`matmul_aligned.c`**:  
   Aligns memory for optimized cache access while maintaining a naive structure.

5. **`test_matmul.c`**:  
   Tests and compares the outputs of all implementations for correctness and performance.

#### Logs (`logs/`)
- Cache miss statistics for each method (e.g., `Aligned_cache_misses.log`, `Blocked_cache_misses.log`).
- Useful for diagnosing memory inefficiencies.

#### Graphs (`graphs/`)
- **`execution_time.png`**: Shows how execution time varies with matrix size, thread count, and block size.
- **`speedup.png`**: Demonstrates the relative performance improvement of optimized methods.

#### Reports (`report/`)
- `cs535_project.docx` and `cs535_project.pdf`: Detailed project documentation, including methodology, results, and analysis.

#### Scripts (`scripts/`)
1. **`cache_analysis_draw.py`**:  
   Generates visualizations of cache performance.

2. **`compare_threading.py`**:  
   Compares execution time and speedup across varying thread counts.

3. **`measure_cache_misses.sh`**:  
   Automates the collection of cache performance data.

4. **`run_vtune_analyses.sh`**:  
   Automates Intel VTune profiling for detailed analysis.

---

## **Optimization Techniques**

1. **Naive Implementation**:  
   - A simple approach using triple-nested loops.
   - Baseline for comparing performance.

2. **Loop Unrolling**:  
   - Reduces loop overhead by unrolling the inner loop (e.g., processing 4 elements per iteration).
   - Improves throughput at the cost of larger binary size.

3. **Cache Blocking (Tiling)**:  
   - Divides matrices into smaller blocks that fit into CPU cache.
   - Significantly improves cache utilization and reduces memory access latency.

4. **Memory Alignment**:  
   - Aligns memory to boundaries (e.g., 64 bytes) for efficient cache line usage.
   - Reduces the number of memory accesses and improves data locality.

---

## **Compilation and Execution**

### Compilation
Use the GNU Compiler Collection (`gcc`) with OpenMP for parallel execution:

gcc -fopenmp <source_file>.c -o <executable_name> -O3

    -fopenmp: Enables OpenMP directives for parallelism.
    -O3: Optimizes the binary for maximum performance.

Execution

Executables accept command-line arguments for customization:
Naive Implementation

./matmul_naive <matrix_size> <num_threads>

Example:

./matmul_naive 1000 4

Blocked Implementation

./matmul_blocked <matrix_size> <num_threads> <block_size>

Example:

./matmul_blocked 1000 4 64

Performance Analysis
Metrics

    Execution Time: Time taken for matrix multiplication.
    Speedup: Ratio of naive execution time to optimized execution time.
    Cache Miss Rates: Percentage of L1, L2, and LLC cache misses.

Tools

    Intel VTune Profiler: Provides detailed insights into CPU and memory performance.
    Python: Scripts for graph generation and analysis.

Key Observations

    Loop Unrolling: Reduced loop control overhead improves performance for larger matrices.
    Cache Blocking: Significantly reduces cache misses, improving memory-bound performance.
    Memory Alignment: Enhances cache utilization by ensuring efficient memory access patterns.

Tools and Libraries Used

    C and OpenMP: For implementation and parallelization.
    Intel VTune Profiler: For detailed profiling of memory and CPU performance.
    Python: For scripting and performance visualization.

Results and Observations

    Execution Time:
        The naive implementation is the slowest due to poor cache utilization.
        Blocking and alignment provide substantial performance improvements.

    Speedup:
        Blocking achieves the highest speedup for large matrices and higher thread counts.

    Cache Miss Rates:
        Blocking reduces cache misses significantly compared to other methods.

Future Work

    Explore GPU-based acceleration for matrix multiplication using CUDA or OpenCL.
    Investigate adaptive tiling strategies based on matrix size and hardware specifications.
    Optimize for NUMA (Non-Uniform Memory Access) systems for even better parallel performance.
