#include <stdio.h>
#include <stdlib.h>

int fib(int n) {
    int n_1, n_2;
    if (n == 0)
        return 0;
    if (n == 1)
        return 1;
        
    #pragma omp task shared(n_1)
    n_1 = fib(n-1);
    #pragma omp task shared(n_2)
    n_2 = fib(n-2);
    #pragma omp taskwait
    return n_1 + n_2;
}

int main(int argc, char const *argv[])
{
    int fib_n;
    if (argc != 2)
        printf("Usage: ./fib N\n");
    
    int n = atoi(argv[1]);
    #pragma omp parallel
   {
        #pragma omp single
        fib_n = fib(n);
   }
    printf("%d\n", fib_n);
    return 0;
}
