import sys
try:
    x=int(input("x:"))
    y=int(input("y: "))
except ValueError:
    print("INVALID ERROR")
    sys.exit(1)

try:
    result = x/y
except ZeroDivisionError:
    print("ERROR CAUGHT")
    sys.exit(1)
print(f"{x} / {y} = {result} ")