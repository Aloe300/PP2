print(5 > 3)
print(2 == 7)

x = 10
if x > 5:
    print("Большое число")

print(bool(0))
print(bool(10))


print(bool(""))
print(bool("hello"))


print(bool([]))
print(bool([1,2,3]))


#That gives us False:
#0 
#0.0
#""
#[]
#{}
#None

x = 6      # 110
x &= 3     # 011
print(x)   #010 = 2

x = 6      # 110
x |= 3     # 011
print(x)   #111 = 7

x = 6      # 110
x ^= 3     # 011
print(x)   #101 = 5


print(x := 3)


a = 5   # 101 
b = 3   # 011 

print(a & b)


result = 2 + 3 * 4
print(result)
