FROM alpine:3.19

RUN apk add --no-cache build-base

COPY ./fib.c .
RUN gcc -o fib fib.c

ENV N=10
CMD time ./fib $N
