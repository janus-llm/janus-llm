from math import sqrt

def main():
    a = 5.0
    b = 10.0
    c = 10.0
    s = (a + b + c) / 2.0
    Area = 0.0
    Cond_1, Cond_2 = False, False

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"c = {c}\n")
 
    Cond_1 = (a > 0.0) and (b > 0.0) and (c > 0.0)
    Cond_2 = (a + b > c) and (a + c > b) and (b + c > a)

    if Cond_1 and Cond_2:
       Area = sqrt(s * (s - a) * (s - b) * (s - c))
       print(f"Triangle area = {Area}")
    else:
       print("ERROR: this is not a triangle!")