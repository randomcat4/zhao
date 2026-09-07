#!/usr/bin/env python3
"""Exact arithmetic checks for round 6 weighted-shadow identities."""
from math import comb


def ibinom(n,k):
    if k<0: return 0
    if k==0: return 1
    z=1
    for t in range(k): z=z*(n-t)//(t+1)
    return z


def det_bareiss(A):
    A=[r[:] for r in A]; n=len(A); prev=1; sign=1
    if not n: return 1
    for k in range(n-1):
        if A[k][k]==0:
            q=next((i for i in range(k+1,n) if A[i][k]),None)
            if q is None: return 0
            A[k],A[q]=A[q],A[k]; sign=-sign
        piv=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=A[i][j]*piv-A[i][k]*A[k][j]
                assert num%prev==0
                A[i][j]=num//prev
        prev=piv
        for i in range(k+1,n): A[i][k]=0
    return sign*A[-1][-1]


def xvecs(r):
    m=r-3; out=[]
    for j in range(2*r-3):
        v=[int(j==0)]+[0]*m
        for s in range(m):
            k=j-s
            if 0<=k<=r: v[1+s]=comb(r,k)
        out.append(v)
    return out


def add(dst,src,c):
    for i,x in enumerate(src): dst[i]+=c*x


def check_r(r):
    xs=xvecs(r); m=r-3; dim=m+1
    for d in range(r):
        lhs=[0]*dim
        for j,x in enumerate(xs): add(lhs,x,(-1)**j*ibinom(r-4-j,d))
        lhs[0]-=ibinom(r-4,d)
        assert lhs==[0]*dim
    F=[0]*dim; F[0]+=ibinom(r-4,r)
    for j,x in enumerate(xs): add(F,x,(-1)**(j+1)*ibinom(r-4-j,r))
    assert F==[0]+[(-1)**(s+1) for s in range(m)]
    for q in range(1,r+1):
        A=[0]*dim; A[0]+=ibinom(r-4-q,r-q)
        for j,x in enumerate(xs):
            add(A,x,(-1)**(j+1)*ibinom(r-4-j-q,r-q))
        assert A==[0]*dim
    M=[]
    for q in range(m):
        row=[]
        for s in range(m): row.append((-1)**(q+s+1)*comb(q+s+3,q))
        M.append(row)
    assert det_bareiss(M)==(-1)**m
    return M


def main():
    for r in range(4,21): check_r(r)
    assert check_r(4)==[[-1]]
    assert check_r(5)==[[-1,1],[4,-5]]
    print('PASS: r=4,...,20; unimodular over-deletion transform verified')
    print('PASS: r=4 gives F4=-theta; r=5 gives F5,F6 matrix [[-1,1],[4,-5]]')

if __name__=='__main__': main()
