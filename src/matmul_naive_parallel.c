/******************************************************************************
 * File: matmul_naive.c
 *
 * Description:
 *   Parallel matrix multiplication using a naive triple-nested loop.
 *
 * Compile (example on Linux with OpenMP):
 *   gcc -fopenmp matmul_naive.c -o matmul_naive -O3
 *
 * Run:
 *   ./matmul_naive <matrix_size> <num_threads>
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include <time.h>
#include <assert.h>

/* Utility: Allocate memory using malloc and initialize to zero */
static inline double* allocate_memory(size_t N)
{
    double *ptr = (double*)malloc(N * sizeof(double));
    if (ptr == NULL) {
        fprintf(stderr, "malloc failed\n");
        exit(EXIT_FAILURE);
    }
    memset(ptr, 0, N * sizeof(double));
    return ptr;
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

/******************************************************************************
 * Naive Parallel Multiplication (OpenMP) with explicit shared/private
 *****************************************************************************/
void matmul_naive(double *A, double *B, double *C, int N, int num_threads)
{
    /* Declare our loop counters and accumulator BEFORE the pragma */
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

    // Allocate memory using standard malloc
    double *A = allocate_memory(N*N);
    double *B = allocate_memory(N*N);
    double *C = allocate_memory(N*N);

    srand((unsigned)time(NULL));

    // Fill A and B with random values
    fill_random(A, N);
    fill_random(B, N);

    double start = get_time_in_seconds();
    matmul_naive(A, B, C, N, num_threads);
    double end   = get_time_in_seconds();

    printf("[Naive] N=%d, threads=%d, time=%f sec\n", N, num_threads, end - start);

    free(A);
    free(B);
    free(C);

    return 0;
}

