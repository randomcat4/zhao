#!/usr/bin/env python3
"""Fresh finite checks for the arithmetic interfaces in the L15 proof."""
from itertools import product
from math import comb
import json

point_rows = [
    (comb(20,t), comb(6,t), -comb(5,t), comb(4,t), -comb(3,t))
    for t in range(4)
]
pair_rows = [
    (comb(19,t), comb(5,t), -comb(4,t), comb(3,t), -comb(2,t))
    for t in range(3)
]
point_solutions=[]
pair_solutions=[]
for values in product(range(5), repeat=4):
    vector=(1,)+values
    if all(sum(a*b for a,b in zip(row,vector))%5==0 for row in point_rows):
        point_solutions.append(values)
    if all(sum(a*b for a,b in zip(row,vector))%5==0 for row in pair_rows):
        pair_solutions.append(values)
assert point_solutions == [(0,1,0,0)]
assert all(a == d for a,b,c,d in pair_solutions)
assert pair_solutions == [(t,(1+3*t)%5,(3*t)%5,t) for t in range(5)]
integer_lift=[(a,d) for a in range(6) for d in range(5) if (a-d)%5==0]
assert integer_lift == [(0,0),(1,1),(2,2),(3,3),(4,4),(5,0)]
class_cases=[]
for r in range(1,8):
    numerator=35-5*r
    if numerator%3==0:
        class_cases.append((r,numerator//3))
assert class_cases == [(1,10),(4,5),(7,0)]
for t in range(6):
    assert (210-20*t)%4==2
print(json.dumps({
    "point_rows": point_rows,
    "point_solutions": point_solutions,
    "pair_rows": pair_rows,
    "pair_solutions": pair_solutions,
    "integer_lift": integer_lift,
    "integral_class_cases_before_simplicity": class_cases,
    "simple_block_class_cases": class_cases[:2],
    "final_mod4_residues": [(t,(210-20*t)%4) for t in range(6)],
    "normal_exit": 0,
}, indent=2))
