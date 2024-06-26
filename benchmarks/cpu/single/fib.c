#include <stdio.h>
#include <stdlib.h>

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
    printf("%d\n", fib(atoi(argv[1])));
    return 0;
}
