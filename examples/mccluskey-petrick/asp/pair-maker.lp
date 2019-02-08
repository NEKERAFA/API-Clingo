#const maxsteps = 0.
step(0..maxsteps).

ex(X, A, V, 0) :- m(X, A, V).
exid(X, S) :- ex(X, _, _, S).

adj(X,Y,S) :- exid(X,S), exid(Y,S), X<Y, #count{A: ex(X,A,V,S), ex(Y,A,W,S), V!=W}=1, step(S).

ex(r(X,Y),A,x,S+1) :- adj(X,Y,S), ex(X,A,V,S), ex(Y,A,W,S), V!=W, step(S), step(S+1).
ex(r(X,Y),A,V,S+1) :- adj(X,Y,S), ex(X,A,V,S), ex(Y,A,V,S), step(S), step(S+1).

primpl(X,A,V) :- exid(X,S), ex(X,A,V,S), not adj(X,_,S), not adj(_,X,S), step(S).
primplid(X) :- primpl(X,A,V).

covers(r(X,Y), X, 1) :- exid(r(X,Y), 1).
covers(r(X,Y), Y, 1) :- exid(r(X,Y), 1).

covers(r(X,Y), Z, S) :- exid(r(X,Y), S), covers(X, Z, S-1), step(S), step(S-1).
covers(r(X,Y), Z, S) :- exid(r(X,Y), S), covers(Y, Z, S-1), step(S), step(S-1).

primplcvr(X, Z) :- primplid(X), covers(X, Z, _).

primplcard(X, C) :- primplcvr(X, Z), C=#count{A: primplcvr(X, A)}.

primplequal(X, Y) :- primplcard(X, C), primplcard(Y, C), X < Y,
            #count{Z: primplcvr(X, Z), primplcvr(Y, Z)}=C.

uprimplid(X) :- primplid(X), not primplequal(X,_).
uprimpl(X,A,V) :- uprimplid(X), primpl(X,A,V).
uprimplcvr(X, Z) :- primplcvr(X, Z), uprimplid(X).

finished(S) :- not adj(_,_,S), adj(_,_,S-1), step(S), step(S-1).

:- not finished(maxsteps).

#show uprimpl/3.
#show uprimplcvr/2.
