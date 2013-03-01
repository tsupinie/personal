from math import sqrt 

def isDivisible(dividend, divisor):
    return float(dividend) / divisor == dividend / divisor

def factors(number):
     for idx in range(1, int(sqrt(number))):
        if isDivisible(number, idx):
            print idx, number / idx

print factors(252)
