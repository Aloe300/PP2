numbers = list(map(int, input().split()))

def square(x):
    return x * x

result = map(square, numbers)

print(*map(square, numbers))