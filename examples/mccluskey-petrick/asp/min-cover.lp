#include <incmode>.

%% t = 0
#program base.
minid(X, 0) :- m(X, _, _).
pimplid(X, 0) :- uprimplid(X).

%% t > 0
#program step(t).
pimplid(X, t) :- pimplid(X, t-1), not essnimplid(X, t-1).
minid(Z, t) :- minid(Z, t-1), not usedminid(Z, t-1).

%% t >= 0
#program check(t).
mincount(Z, C, t) :- minid(Z, t), C=#count{X:uprimplcvr(X, Z)}.
essnimplid(X, t) :- uprimplcvr(X, Z), mincount(Z, 1, t).
usedminid(Z, t) :- essnimplid(X, t), uprimplcvr(X, Z).
fullcover(t) :- minid(Z, t), usedminid(Z, t).

:- query(t), essnimplid(X, t).

essnimplid(X) :- essnimplid(X, t).
essnimplcvr(X, Z) :- essnimplid(X), uprimplcvr(X, Z).
essnimpl(X, A, V) :- essnimplid(X), uprimpl(X, A, V).

leftimplid(X) :- uprimplid(X), not essnimplid(X).
leftimplcvr(X, Z) :- leftimplid(X), uprimplcvr(X, Z).
leftimpl(X, A, V) :- leftimplid(X), uprimpl(X, A, V).

#show fullcover/1.
#show essnimplid/1.
#show essnimplcvr/2.
#show essnimpl/3.
#show leftimplid/1.
#show leftimplcvr/2.
#show leftimpl/3.
