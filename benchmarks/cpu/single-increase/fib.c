#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>
struct timespec start, end;

int fib(int n) {
    if (n == 0)
        return 0;
    if (n == 1)
        return 1;
    return fib(n-1) + fib(n-2);
}

int main(int argc, char const *argv[])
{
    if (argc != 2)
        printf("Usage: ./fib N\n");
    printf("The argument supplied is %s\n", argv[1]);
    sleep(5);
    for (int i = 2; i < atoi(argv[1]); i++) {
        clock_gettime(CLOCK_MONOTONIC_RAW, &start);
        fib(i);
        clock_gettime(CLOCK_MONOTONIC_RAW, &end);
        printf("%d,%lu,%ld\n", i, (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_nsec - start.tv_nsec) / 1000, time(NULL));
        sleep(5);
    }
    return 0;
}
