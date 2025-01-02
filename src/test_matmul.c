#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <omp.h>

/******************************************************************************
 * 1. Define or paste in the four matmul functions we wrote: Naive, Unrolled,
 *    Blocked, and Aligned.
 *****************************************************************************/

void matmul_naive(double *A, double *B, double *C, int N, int num_threads);
void matmul_unrolled(double *A, double *B, double *C, int N, int num_threads);
void matmul_blocked(double *A, double *B, double *C, int N, int block_size, int num_threads);
void matmul_aligned(double *A, double *B, double *C, int N, int num_threads);

/******************************************************************************
 * 2. Implementations
 *    - We declare i, j, k (and block indexes) before the pragma for clarity.
 *****************************************************************************/

/* Naive */
void matmul_naive(double *A, double *B, double *C, int N, int num_threads)
{
    int i, j, k;
    double sum;

#pragma omp parallel for num_threads(num_threads) \
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

/* Unrolled */
void matmul_unrolled(double *A, double *B, double *C, int N, int num_threads)
{
    int i, j, k;
    double sum;

#pragma omp parallel for num_threads(num_threads) \
    shared(A, B, C, N) private(i, j, k, sum)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            sum = 0.0;
            k   = 0;
            /* Unroll by 4 (if N=5, unrolling is minimal but demonstrates the idea). */
            for (; k <= N - 4; k += 4) {
                sum += A[i*N + k]   * B[k*N + j]
                     + A[i*N + k+1] * B[(k+1)*N + j]
                     + A[i*N + k+2] * B[(k+2)*N + j]
                     + A[i*N + k+3] * B[(k+3)*N + j];
            }
            /* Handle leftover elements */
            for (; k < N; k++) {
                sum += A[i*N + k] * B[k*N + j];
            }
            C[i*N + j] = sum;
        }
    }
}

/* Blocked */
void matmul_blocked(double *A, double *B, double *C, int N, int block_size, int num_threads)
{
    int iBlock, jBlock, kBlock;
    int i, j, k;
    double sum;

#pragma omp parallel for num_threads(num_threads) collapse(2) \
    shared(A, B, C, N, block_size) private(iBlock, jBlock, kBlock, i, j, k, sum)
    for (iBlock = 0; iBlock < N; iBlock += block_size) {
        for (jBlock = 0; jBlock < N; jBlock += block_size) {
            for (kBlock = 0; kBlock < N; kBlock += block_size) {
                for (i = iBlock; i < iBlock + block_size && i < N; i++) {
                    for (j = jBlock; j < jBlock + block_size && j < N; j++) {
                        /* Start with current value in C (or 0.0 if you're always overwriting) */
                        sum = C[i*N + j];
                        for (k = kBlock; k < kBlock + block_size && k < N; k++) {
                            sum += A[i*N + k] * B[k*N + j];
                        }
                        C[i*N + j] = sum;
                    }
                }
            }
        }
    }
}

/* Aligned (naive structure, but we assume memory is aligned outside) */
void matmul_aligned(double *A, double *B, double *C, int N, int num_threads)
{
    int i, j, k;
    double sum;

#pragma omp parallel for num_threads(num_threads) \
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

/******************************************************************************
 * 3. Main function: do a 5x5 test with random or small integer data,
 *    compare each result to the "naive" approach.
 *****************************************************************************/

/* Utility function to fill a matrix (size NxN) with random doubles [0..1]. */
void fill_random(double *mat, int N)
{
    for (int i = 0; i < N*N; i++) {
        mat[i] = (double)rand() / (double)RAND_MAX;
    }
}

/* Compute the sum of squared differences between two NxN matrices. */
double compute_diff(double *X, double *Y, int N)
{
    double diff = 0.0;
    for (int i = 0; i < N*N; i++) {
        double d = X[i] - Y[i];
        diff += d * d;
    }
    return diff;
}

int main(void)
{

    const int N = 5;
    const int num_threads = 2;    
    const int block_size  = 2;    /* typical block size for 5 is small, just for demo */

    /* Seed random generator. If you want reproducible results, use a fixed seed. */
    srand((unsigned) time(NULL));

    /* Allocate arrays on the heap just for demonstration (or stack is okay for 5x5) */
    double *A         = (double*) calloc(N*N, sizeof(double));
    double *B         = (double*) calloc(N*N, sizeof(double));

    /* We'll store results from each method in separate arrays. */
    double *C_naive    = (double*) calloc(N*N, sizeof(double));
    double *C_unrolled = (double*) calloc(N*N, sizeof(double));
    double *C_blocked  = (double*) calloc(N*N, sizeof(double));
    double *C_aligned  = (double*) calloc(N*N, sizeof(double));

    /* 1) Fill A and B with random data. */
    fill_random(A, N);
    fill_random(B, N);

    /* 2) NAIVE: C_naive = A * B */
    matmul_naive(A, B, C_naive, N, num_threads);

    /* 3) UNROLLED: C_unrolled = A * B */
    matmul_unrolled(A, B, C_unrolled, N, num_threads);

    /* 4) BLOCKED: C_blocked = A * B */
    matmul_blocked(A, B, C_blocked, N, block_size, num_threads);

    /* 5) ALIGNED: C_aligned = A * B */
    matmul_aligned(A, B, C_aligned, N, num_threads);

    /* 6) Compare each result to naive's result. */
    double diff_unrolled = compute_diff(C_naive, C_unrolled, N);
    double diff_blocked  = compute_diff(C_naive, C_blocked, N);
    double diff_aligned  = compute_diff(C_naive, C_aligned, N);

    /* Print the differences. Ideally all near zero. */
    printf("Difference (Naive vs. Unrolled) = %e\n", diff_unrolled);
    printf("Difference (Naive vs. Blocked)  = %e\n", diff_blocked);
    printf("Difference (Naive vs. Aligned)  = %e\n", diff_aligned);

    /* Check if they are small enough to be considered correct. 
       For a 5x5 random test, the results should match EXACTLY for double (unless 
       there's a summation ordering difference). Typically, a small floating 
       tolerance is used in real HPC code, e.g. if (diff < 1e-12) ...
    */
    if (diff_unrolled < 1e-12 && diff_blocked < 1e-12 && diff_aligned < 1e-12) {
        printf("All methods match the naive approach for N=5.\n");
    } else {
        printf("Some methods differ from naive result. Investigate!\n");
    }

    /* 7) Cleanup */
    free(A);
    free(B);
    free(C_naive);
    free(C_unrolled);
    free(C_blocked);
    free(C_aligned);

    return 0;
}
