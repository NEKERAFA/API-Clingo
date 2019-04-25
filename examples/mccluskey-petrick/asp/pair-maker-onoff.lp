#include <incmode>.

symbol(0;1;x).
pair(0, 1, x).

pair(Y, X, Z) :- pair(X, Y, Z).
partial(X, Y, X) :- pair(_,X,Y).
partial(Y, X, X) :- partial(X, Y, X).

belongs(X, Y) :- pair(X,_,Y).
belongs(X, Y) :- pair(_,X,Y).

unbelongs(X,Y) :- symbol(X), symbol(Y), X!=Y, not belongs(X,Y).

atom(A) :- on(X,A,V).

%% t = 0
#program base.
holds(on(X,A,V), 0):- on(X, A, V).

%% t > 0
#program step(t).
holds(on((X,A), A, x), t) :- holds(on(X,A,V),t-1), V!=x, not nadj(X,_,A,t-1).
holds(on((X,A), B, V), t) :- holds(on(X,B,V),t-1), B!=A, onid((X,A), t), not nadj(X,_,A,t-1).


%% t >= 0
#program check(t).
onid(X,t) :- holds(on(X,A,V),t).
offid(X) :- off(X,A,V).

nadj(X,Y,A,t) :- holds(on(X,A,V),t), off(Y,A,W), pair(V,W,x),
                0=#count{ B: holds(on(X,B,BV),t), off(Y,B,BW), A!=B, pair(BV, BW, x) }.

:- query(t), nadj(X,Y,A,t).
:- query(t), not primeid(_,t).

primeid(X,t) :- onid(X,t-1), not onid((X,_), t).

%% Esto usa t como delimitador para comparar y seguramente no funcione con - en input
equalid(X,Y) :- primeid(X,_), primeid(Y,_), X < Y,
                0=#count{ A: holds(on(X,A,V),_), holds(on(Y,A,W),_), V!=W  }.

%% Puede que esto haya que retocarlo
uprimplid(X) :- primeid(X,_), not equalid(_,X).
uprimpl(X,A,V) :- uprimplid(X), holds(on(X, A, V), _).

uprimplcvr(X,Z) :- uprimplid(X), on(Z,_,_),
              0=#count{ A: uprimpl(X,A,V), on(Z,A,W), unbelongs(W,V) }.

#show uprimplid/1.
#show uprimpl/3.
#show uprimplcvr/2.
