#include <incmode>.

%% t = 0
#program base.
holds(m(X,A,V), 0):- m(X, A, V).
covers(X, X, 0) :- m(X, A, V).

%% t > 0
#program step(t).
holds(m((X,Y),A,x), t) :- adj(X,Y,t-1), holds(m(X,A,V),t-1), holds(m(Y,A,W),t-1), V!=W.
holds(m((X,Y),A,V), t) :- adj(X,Y,t-1), holds(m(X,A,V),t-1), holds(m(Y,A,V),t-1).

%% t >= 0
#program check(t).
id(X) :- holds(m(X,A,V),t).
adj(X,Y,t) :- id(X), id(Y), X<Y, #count{A: holds(m(X,A,V),t), holds(m(Y,A,W),t), V!=W}=1.
covers((X,Y), X, 1) :- id((X,Y)).
covers((X,Y), Y, 1) :- id((X,Y)).
covers((X,Y), Z, t) :- id((X,Y)), covers(X, Z, t-1).
covers((X,Y), Z, t) :- id((X,Y)), covers(Y, Z, t-1).

primpl(X,A,V) :- id(X), holds(m(X,A,V),t), not adj(X,_,t), not adj(_,X,t).
primplid(X) :- primpl(X,A,V).
primplcvr(X, Z) :- primplid(X), covers(X,Z,t).
primplcard(X, C) :- primplcvr(X, Z), C=#count{A: primplcvr(X, A)}.
primplequal(X, Y) :- primplcard(X, C), primplcard(Y, C), X < Y,
            #count{Z: primplcvr(X, Z), primplcvr(Y, Z)}=C.

uprimplid(X) :- primplid(X), primplequal(X, _), not primplequal(_, X).
uprimpl(X, A, V) :- primpl(X, A, V), uprimplid(X).
uprimplcvr(X, Z) :- uprimplid(X), primplcvr(X, Z).

:- query(t), adj(X,Y,t).

#show uprimplid/1.
#show uprimpl/3.
#show uprimplcvr/2.
