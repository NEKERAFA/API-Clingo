#const max_steps = 0.
step(0..max_steps).

ex(X, A, V, 0) :- m(X, A, V).
ex_id(X, S) :- ex(X, _, _, S).

adj(X,Y,S) :- ex_id(X,S), ex_id(Y,S), X<Y, #count{A: ex(X,A,V,S), ex(Y,A,W,S), V!=W}=1, step(S).

ex(r(X,Y),A,x,S+1) :- adj(X,Y,S), ex(X,A,V,S), ex(Y,A,W,S), V!=W, step(S), step(S+1).
ex(r(X,Y),A,V,S+1) :- adj(X,Y,S), ex(X,A,V,S), ex(Y,A,V,S), step(S), step(S+1).

pr_impl(X,A,V) :- ex_id(X,S), ex(X,A,V,S), not adj(X,_,S), not adj(_,X,S), step(S).
pr_impl_id(X) :- pr_impl(X,A,V).

covers(r(X,Y), X, 1) :- ex_id(r(X,Y), 1).
covers(r(X,Y), Y, 1) :- ex_id(r(X,Y), 1).

covers(r(X,Y), Z, S) :- ex_id(r(X,Y), S), covers(X, Z, S-1), step(S), step(S-1).
covers(r(X,Y), Z, S) :- ex_id(r(X,Y), S), covers(Y, Z, S-1), step(S), step(S-1).

pr_impl_covers(X, Z) :- pr_impl_id(X), covers(X, Z, _).

pr_impl_card(X, C) :- pr_impl_covers(X, Z), C=#count{A: pr_impl_covers(X, A)}.

pr_impl_equal(X, Y) :- pr_impl_card(X, C), pr_impl_card(Y, C), X < Y,
            #count{Z: pr_impl_covers(X, Z), pr_impl_covers(Y, Z)}=C.

pr_impl_unique_id(X) :- pr_impl_id(X), not pr_impl_equal(X,_).
pr_impl_unique(X,A,V) :- pr_impl_unique_id(X), pr_impl(X,A,V).

finished(S) :- not adj(_,_,S), adj(_,_,S-1), step(S), step(S-1).

:- not finished(max_steps).

#show pr_impl_unique/3.
#show pr_impl_covers/2.
