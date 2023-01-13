n = int(input())
a = 1
b = 1
print(a)
print(b)
for i in range(2,n):
    c = a+b
    b = a
    a = c
    print(c)