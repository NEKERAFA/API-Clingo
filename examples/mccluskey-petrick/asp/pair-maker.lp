#include <incmode>.

symbol(0;1;x).
pair(0, 1, x).

pair(Y, X, Z) :- pair(X, Y, Z).
partial(X, Y, X) :- pair(_,X,Y).
partial(Y, X, X) :- partial(X, Y, X).

belongs(X, Y) :- pair(X,_,Y).
belongs(X, Y) :- pair(_,X,Y).

unbelongs(X,Y) :- symbol(X), symbol(Y), X!=Y, not belongs(X,Y).

%% t = 0
#program base.
holds(m(X,A,V), 0):- m(X, A, V).
covers(X, X, 0) :- m(X, A, V).

%% t > 0
#program step(t).
holds(m((X,Y),A,x), t) :- adj(X,Y,t-1), holds(m(X,A,V),t-1), holds(m(Y,A,W),t-1), pair(V, W, x).
holds(m((X,Y),A,Z), t) :- adj(X,Y,t-1), holds(m(X,A,V),t-1), holds(m(Y,A,W),t-1), partial(V, W, Z).
holds(m((X,Y),A,V), t) :- adj(X,Y,t-1), holds(m(X,A,V),t-1), holds(m(Y,A,V),t-1).
holds(m(X,A,V), t) :- subsum(X,Y,t-1), holds(m(X,A,V),t-1).

usedatomvalue(X, A, V, t) :- holds(m((X,Y),A,x), t), holds(m(X,A,V),t-1).
usedatomvalue(Y, A, V, t) :- holds(m((X,Y),A,x), t), holds(m(Y,A,V),t-1).
usedatomvalue(X, A, V, t) :- holds(m((X,Y),A,V), t), V!=x.
usedatomvalue(Y, A, V, t) :- holds(m((X,Y),A,V), t), V!=x.
usedatomvalue(Y, A, V, t) :- subsum(X,Y,t-1), holds(m(Y,A,V),t-1).

unmark(X, t) :- holds(m(X, A, V), t-1), not usedatomvalue(X, A, V, t).
mark(X, t) :- id(X), not unmark(X, t).

covers((X,Y), Z, t) :- id((X,Y)), covers(X, Z, t-1), not unmark(X, t).
covers((X,Y), Z, t) :- id((X,Y)), covers(Y, Z, t-1), not unmark(Y, t).

%% t >= 0
#program check(t).
id(X,t) :- holds(m(X,A,V),t).
id(X) :- id(X,t).
ones(X, C) :- id(X), C=#count{A: holds(m(X, A, 1), t) }.
exes(X, C) :- id(X), C=#count{A: holds(m(X, A, x), t) }.

adj(X,Y,t) :- id(X,t), id(Y,t),
              #count{A: holds(m(X,A,V),t), holds(m(Y,A,W),t), pair(V, W, x)}=1,
              #count{A: holds(m(X,A,V),t), holds(m(Y,A,W),t), unbelongs(V,W), not pair(V, W, x) }=0.

subsum(X,Y,t) :- id(X,t), id(Y,t), exes(X, XCX), exes(Y, YCX), X>Y, XCX>YCX,
                #count{A: holds(m(X,A,V),t), holds(m(Y,A,W),t), pair(V, W, x)}=0.

unmark(X, t) :- id(X), not adj(X,_,_), not adj(_,X,_), not subsum(_,X,_).

:- query(t), adj(X,Y,t).
:- query(t), subsum(X,Y,t).

primpl(X) :- query(t), unmark(X,t).
primplequal(X, Y) :- exes(X, C), exes(Y, C), X < Y,
            #count{Z: covers(X, Z, t), covers(Y, Z, t) }=(2**C).

uprimplid(X) :- primpl(X), primplequal(X, _), not primplequal(_, X).
uprimplid(X) :- primpl(X), not primplequal(X, _), not primplequal(_, X).
uprimpl(X, A, V) :- holds(m(X,A,V), _), uprimplid(X).
uprimplcvr(X, Z) :- uprimplid(X), covers(X, Z, _), not dcid(Z).

#show uprimplid/1.
#show uprimpl/3.
#show uprimplcvr/2.
