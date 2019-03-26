#include <incmode>.

%% t = 0
#program base.
implid(X, 0) :- uprimplid(X).
mintermid(Z, 0) :- uprimplcvr(X, Z).
covers(X, Z, 0) :- uprimplcvr(X, Z).

%% t > 0
#program step(t).
implid(X, t) :- implid(X, t-1), not essnimplid(X, t-1).
mintermid(Z, t) :- mintermid(Z, t-1), not usedminid(Z, t-1).
covers(X, Z, t) :- covers(X, Z, t-1), not usedminid(Z, t-1).
fullcover :- not notfull(t).

%% t >= 0
#program check(t).
timescovered(Z, C, t) :- mintermid(Z, t), C=#count{ X: covers(X, Z, t) }.
essnimplid(X, t) :- covers(X, Z, t), timescovered(Z, 1, t).
usedminid(Z, t) :- essnimplid(X, t), covers(X, Z, t).
notfull(t) :- mintermid(Z, t).

:- query(t), essnimplid(X, t).

leftimplid(X) :- query(t), implid(X,t), notfull(t).
leftimplcvr(X, Z) :- leftimplid(X), covers(X, Z, t).
leftimpl(X, A, V) :- leftimplid(X), uprimpl(X, A, V).

essnimplid(X) :- essnimplid(X, _).
essnimplcvr(X, Z) :- essnimplid(X), covers(X, Z, t).
essnimpl(X, A, V) :- essnimplid(X), uprimpl(X, A, V).
