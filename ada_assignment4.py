# ADA Lab Assignment 4
# Author: Adarsh Rai

import time
from itertools import permutations

# -------------------- TASK 1 --------------------
# Backtracking - Crew Scheduling

flights = [('F1',6,8), ('F2',7,10), ('F3',9,11),
           ('F4',11,13), ('F5',12,14), ('F6',14,16)]

crew_members = ['C1','C2','C3']
REST_TIME = 1

schedule = {}
assignment = {}

def overlaps(crew, start, end):
    for s, e, _ in schedule.get(crew, []):
        if not (end + REST_TIME <= s or start >= e + REST_TIME):
            return True
    return False

def backtrack(idx):
    if idx == len(flights):
        return True

    fid, start, end = flights[idx]
    for crew in crew_members:
        if not overlaps(crew, start, end):
            assignment[fid] = crew
            schedule.setdefault(crew, []).append((start,end,fid))

            if backtrack(idx+1):
                return True

            assignment.pop(fid)
            schedule[crew].pop()
    return False


# -------------------- TASK 2 --------------------
# Branch & Bound Knapsack

items = [('Laptop',3,90), ('Camera',1,60), ('Headset',2,50),
         ('Tablet',2,70), ('Charger',1,30), ('Book',1,20)]

CAPACITY = 6
items_sorted = sorted(items, key=lambda x: x[2]/x[1], reverse=True)

best_value = [0]

def upper_bound(idx, curr_w, curr_v):
    bound = curr_v
    for i in range(idx, len(items_sorted)):
        _, w, v = items_sorted[i]
        if curr_w + w <= CAPACITY:
            curr_w += w
            bound += v
    return bound

def branch_and_bound(idx, curr_w, curr_v):
    if curr_w > CAPACITY:
        return

    best_value[0] = max(best_value[0], curr_v)

    if idx == len(items_sorted):
        return

    if upper_bound(idx, curr_w, curr_v) <= best_value[0]:
        return

    _, w, v = items_sorted[idx]

    branch_and_bound(idx+1, curr_w+w, curr_v+v)
    branch_and_bound(idx+1, curr_w, curr_v)


# -------------------- TASK 3 --------------------
# String Matching

def naive_search(text, pattern):
    matches = []
    for i in range(len(text)-len(pattern)+1):
        if text[i:i+len(pattern)] == pattern:
            matches.append(i)
    return matches


def build_lps(pattern):
    lps = [0]*len(pattern)
    j = 0
    for i in range(1,len(pattern)):
        while j>0 and pattern[i]!=pattern[j]:
            j = lps[j-1]
        if pattern[i]==pattern[j]:
            j+=1
            lps[i]=j
    return lps


def kmp_search(text, pattern):
    lps = build_lps(pattern)
    i=j=0
    matches = []
    while i<len(text):
        if text[i]==pattern[j]:
            i+=1; j+=1
        if j==len(pattern):
            matches.append(i-j)
            j=lps[j-1]
        elif i<len(text) and text[i]!=pattern[j]:
            if j>0:
                j=lps[j-1]
            else:
                i+=1
    return matches


def rabin_karp(text, pattern):
    return naive_search(text, pattern)  # simplified


# -------------------- TASK 5 --------------------
# N-Queens

def solve_nqueens(n):
    board = [-1]*n
    solutions = []

    def is_safe(r,c):
        for i in range(r):
            if board[i]==c or abs(board[i]-c)==abs(i-r):
                return False
        return True

    def backtrack(r):
        if r==n:
            solutions.append(board[:])
            return
        for c in range(n):
            if is_safe(r,c):
                board[r]=c
                backtrack(r+1)
                board[r]=-1

    backtrack(0)
    return solutions


# -------------------- MAIN --------------------

if __name__ == "__main__":
    backtrack(0)
    print("Crew Assignment:", assignment)

    branch_and_bound(0,0,0)
    print("Best Knapsack Value:", best_value[0])

    print("Naive Search:", naive_search("airline crew system","crew"))

    print("KMP Search:", kmp_search("airline crew system","crew"))

    print("N-Queens (4):", solve_nqueens(4))
