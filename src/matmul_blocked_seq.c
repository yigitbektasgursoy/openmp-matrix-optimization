#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <assert.h>

/* We make BLOCK_SIZE a variable read from the command line. */
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

/******************************************************************************
 * Cache-blocked multiplication:
 *   Break the matrices into smaller tiles (blocks) to improve cache locality.
 *****************************************************************************/
void matmul_blocked(double *A, double *B, double *C,
                    int N, int block_size)
{
    /* We have block loop indices and normal loop indices */
    int iBlock, jBlock, kBlock;
    int i, j, k;
    double sum;

    for (iBlock = 0; iBlock < N; iBlock += block_size) {
        for (jBlock = 0; jBlock < N; jBlock += block_size) {
            for (kBlock = 0; kBlock < N; kBlock += block_size) {

                for (i = iBlock; i < iBlock + block_size && i < N; i++) {
                    for (j = jBlock; j < jBlock + block_size && j < N; j++) {
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


int main(int argc, char* argv[])
{
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <matrix_size> <block_size>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int N           = atoi(argv[1]);
    int block_size  = atoi(argv[2]);

    double *A = aligned_alloc_doubles(N*N, 64);
    double *B = aligned_alloc_doubles(N*N, 64);
    double *C = aligned_alloc_doubles(N*N, 64);

    srand((unsigned)time(NULL));

    fill_random(A, N);
    fill_random(B, N);

    double start = get_time_in_seconds();
    matmul_blocked(A, B, C, N, block_size);
    double end   = get_time_in_seconds();

    printf("[Blocked] N=%d, block_size=%d, time=%f sec\n",
           N, block_size, end - start);

    free(A);
    free(B);
    free(C);

    return 0;
}

