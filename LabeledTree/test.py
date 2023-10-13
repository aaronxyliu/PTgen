# Minify pTree size for each version

from tree import *

def get_equivalence(numlist):
        r = 0
        eq = []    # eq[i] = {1, 3, 5} means 1, 3, 5 belong to a equivalence class
        n = len(numlist)
        for i in range(n):
            eq.append({i})
        max_eq_size = 1
        neq = [set()] * n
        U = set(range(n))
        while True:
            r += 1
            for i in range(n):
                # Find the next j if any, starting from i + 1, wrapped around after n if necessary, such that j /∈ eq(i) ∪ neq(i).
                J = U - (eq[i] | neq[i])
                for j in J:
                # if len(J): # if such a j is found
                #     j = min(J)
                #     if i + 1 in J:
                #         j = i + 1
                    # j = J.pop()
                    if numlist[i] == numlist[j]:
                        temp = eq[i] | eq[j]
                        for x in temp:
                            eq[x] = eq[i] | eq[j]
                            neq[x] = neq[i] | neq[j]
                            if len(eq[x]) > max_eq_size:
                                max_eq_size = len(eq[x])
                    else:
                        for x in eq[i]:
                            neq[x] = neq[x] | eq[j]
                        for y in eq[j]:
                            neq[y] = neq[y] | eq[i]
            if max_eq_size >= (n - 1) / r:
                break
        return eq

if __name__ == '__main__':
    L = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 
         13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
         25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 
         37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 
         49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
         61, 62, 63, 64, 65, 65, 67, 68, 69, 70, 71, 72, 
         73, 74, 75, 76, 77, 78, 78, 80, 81, 82, 83, 82, 83, 
         86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98,
           99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
             109, 110, 111]
    # L = [1, 2, 2, 2, 3, 4, 5, 6 ,5, 5]
    eq = get_equivalence(L)
    print(eq)

   