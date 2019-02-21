overlapid(X, Y) :- leftimplcvr(X,Z), leftimplcvr(Y,Z), X<Y.

1{ selectid(X):leftimplid(X) }.

selectimplcvr(X, Z) :- selectid(X), leftimplcvr(X, Z).
selectimpl(X, A, V) :- selectid(X), leftimpl(X, A, V).

fullcover :- C=#count{X:leftimplid(X)}, D=#count{Z:selectimplcvr(_,Z)}, C=D.

:- selectid(X), selectid(Y), X<Y, overlapid(X,Y).
:- not fullcover.

#show selectid/1.
#show selectimplcvr/2.
#show selectimpl/3.
#show fullcover/0.
