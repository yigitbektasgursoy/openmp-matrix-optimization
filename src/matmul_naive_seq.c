#include <stdio.h>
#include <stdlib.h>
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
void matmul_naive(double *A, double *B, double *C, int N)
{
    /* Declare our loop counters and accumulator BEFORE the pragma */
    int i, j, k;
    double sum;

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
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <matrix_size>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int N           = atoi(argv[1]);

    // Allocate memory using standard malloc
    double *A = allocate_memory(N*N);
    double *B = allocate_memory(N*N);
    double *C = allocate_memory(N*N);

    srand((unsigned)time(NULL));

    // Fill A and B with random values
    fill_random(A, N);
    fill_random(B, N);

    double start = get_time_in_seconds();
    matmul_naive(A, B, C, N);
    double end   = get_time_in_seconds();

    printf("[Naive] N=%d, time=%f sec\n", N, end - start);

    free(A);
    free(B);
    free(C);

    return 0;
}

