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
```bash
gcc -fopenmp <source_file>.c -o <executable_name> -O3
