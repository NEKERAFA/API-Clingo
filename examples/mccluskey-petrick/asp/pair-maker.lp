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
ones(X, C) :- id(X), C=#count{A: holds(m(X, A, 1), t) }.
exes(X, C) :- id(X), C=#count{A: holds(m(X, A, x), t) }.

adj(X,Y,t) :- ones(X, C), ones(Y, C+1), X<Y,
                #count{A: holds(m(X,A,V),t), holds(m(Y,A,W),t), V!=W}=1.

covers((X,Y), Z, t) :- id((X,Y)), covers(X, Z, t-1).
covers((X,Y), Z, t) :- id((X,Y)), covers(Y, Z, t-1).

used(X) :- adj(X,Y, _).
used(Y) :- adj(X,Y, _).

unused(X) :- id(X), not used(X).
unusedequal(X, Y) :- exes(X, C), exes(Y, C), X < Y,
            #count{Z: covers(X, Z, t), covers(Y, Z, t) }=(2**C).

uprimplid(X) :- unused(X), unusedequal(X, _), not unusedequal(_, X).
uprimplid(X) :- unused(X), not unusedequal(X, _), not unusedequal(_, X).
uprimpl(X, A, V) :- holds(m(X,A,V), _), uprimplid(X).
uprimplcvr(X, Z) :- uprimplid(X), covers(X, Z, _), not dcid(Z).

:- query(t), adj(X,Y,t).

#show uprimplid/1.
#show uprimpl/3.
#show uprimplcvr/2.
