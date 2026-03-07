def squares_upto(n):
    for i in range(1, n + 1):
        yield i * i
n = int(input())
for a in squares_upto(n):
    print(a)

#######################################################

def evens(n):
    for x in range(0, n + 1, 2):
        yield x
n = int(input())
print(*evens(n), sep=",")

#######################################################

def div_by_3_and_4(n):
    for x in range(0, n + 1):
        if x % 12 == 0:
            yield x
n = int(input())
print(*div_by_3_and_4(n), sep=" ")

#######################################################

def squares(a, b):
    for x in range(a, b + 1):
        yield x * x
a = int(input())
b = int(input())
for v in squares(a, b):
    print(v)

#######################################################

def countdown(n):
    for x in range(n, -1, -1):
        yield x

n = int(input())
print(*countdown(n), sep=" ")