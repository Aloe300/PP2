if 2 > 1:
    print("True")

if 3 > 2:
    print("True")
else:
    print("False")

n = int(input())
if n % 2 == 0:
    print("Even")
else:
    print("Odd")

print("Even" if int(input()) % 2 == 0 else "Odd")

n = int(input())

while n != 0:
    if n % 2 == 0:
        print("Even")
    else:
        print("Odd")
    
    n = int(input())
