# Matrix Multiplication Optimization Project

This project demonstrates various optimization techniques for matrix multiplication using C and OpenMP. It evaluates performance across multiple methods, including naive implementation, loop unrolling, cache blocking, and explicit memory alignment.

---

## **Project Structure**

### **Directories**
- **`bin/`**: Compiled executables for the implemented methods.
- **`graphs/`**: Performance visualizations such as execution time and speedup charts.
- **`logs/`**: Logs containing performance metrics, including cache misses and threading details.
- **`report/`**: Detailed project reports in `.docx` and `.pdf` formats.
- **`scripts/`**: Python and shell scripts for automation and analysis.
- **`src/`**: Source code files for the matrix multiplication methods.
- **`vtune_results/`**: Results from Intel VTune profiler for performance analysis.

### **Files**
#### Source Code (`src/`)
- `matmul_naive.c`: Implements a naive matrix multiplication algorithm.
- `matmul_unrolled.c`: Adds loop unrolling to optimize performance.
- `matmul_blocked.c`: Implements cache blocking to enhance memory locality.
- `matmul_aligned.c`: Aligns memory for better cache performance.
- `test_matmul.c`: Tests and compares all methods for correctness and performance.

#### Logs (`logs/`)
- Logs such as `Aligned_cache_misses.log` and `Blocked_cache_misses.log` capture performance metrics like cache misses.

#### Graphs (`graphs/`)
- Visualizations such as `execution_time.png` and `speedup.png` illustrate the performance differences among methods.

#### Reports (`report/`)
- `cs535_project.docx` and `cs535_project.pdf` provide detailed project documentation, including results and analysis.

#### Scripts (`scripts/`)
- `cache_analysis_draw.py`: Generates visualizations of cache usage.
- `compare_threading.py`: Compares performance across different thread counts.
- `measure_cache_misses.sh`: Automates cache miss analysis.
- `run_vtune_analyses.sh`: Automates VTune profiler runs.

---

## **Compilation and Execution**

### Compilation
Use the `gcc` compiler with OpenMP support:
```bash
gcc -fopenmp <source_file>.c -o <executable_name> -O3
