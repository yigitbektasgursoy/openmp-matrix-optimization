/******************************************************************************
 * File: matmul_aligned.c
 *
 * Description:
 *   Demonstrates the effect of explicit memory alignment for parallel 
 *   matrix multiplication. Here we apply alignment but otherwise use 
 *   a naive loop structure. You can also combine alignment with 
 *   unrolling or blocking.
 *
 * Compile:
 *   gcc -fopenmp matmul_aligned.c -o matmul_aligned -O3
 *
 * Run:
 *   ./matmul_aligned <matrix_size> <num_threads>
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include <time.h>
#include <assert.h>

static inline double* aligned_alloc_doubles(size_t N, size_t alignment)
{
    void *ptr = NULL;
    int ret = posix_memalign(&ptr, alignment, N * sizeof(double));
    if (ret != 0) {
        fprintf(stderr, "posix_memalign failed\n");
        exit(EXIT_FAILURE);
    }
    memset(ptr, 0, N * sizeof(double));
    return (double*)ptr;
}

static inline void fill_random(double *mat, int N)
{
    for (int i = 0; i < N*N; i++) {
        mat[i] = (double)rand() / (double)RAND_MAX;
    }
}

static inline double get_time_in_seconds()
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1.0e-9;
}

void matmul_aligned(double *A, double *B, double *C, int N, int num_threads)
{
    int i, j, k;
    double sum;

#pragma omp parallel for num_threads(num_threads)        \
    shared(A, B, C, N) private(i, j, k, sum)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            sum = 0.0;
            for (k = 0; k < N; k++) {
                sum += A[i*N + k] * B[k*N + j];
            }
            C[i*N + j] = sum;
        }
    }
}

int main(int argc, char* argv[])
{
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <matrix_size> <num_threads>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int N           = atoi(argv[1]);
    int num_threads = atoi(argv[2]);

    double *A = aligned_alloc_doubles(N*N, 64);
    double *B = aligned_alloc_doubles(N*N, 64);
    double *C = aligned_alloc_doubles(N*N, 64);

    srand((unsigned)time(NULL));

    fill_random(A, N);
    fill_random(B, N);

    double start = get_time_in_seconds();
    matmul_aligned(A, B, C, N, num_threads);
    double end   = get_time_in_seconds();

    printf("[Aligned] N=%d, threads=%d, time=%f sec\n", N, num_threads, end - start);

    free(A);
    free(B);
    free(C);

    return 0;
}
