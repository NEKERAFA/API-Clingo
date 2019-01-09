m_id(X) :- m(X, _, _).

adj_minterm(X,Y) :- m_id(X), m_id(Y), X<Y, #count{A: m(X,A,V), m(Y,A,W), V!=W}=1.

nm(r(X,Y),A,x) :- adj_minterm(X,Y), m(X,A,V), m(Y,A,W), V!=W.
nm(r(X,Y),A,V) :- adj_minterm(X,Y), m(X,A,V), m(Y,A,V).

pr_impl(X,A,V) :- m_id(X), m(X,A,V), not nm(r(X,_),_,_), not nm(r(_,X),_,_).

finished :- not adj_minterm(_,_).

#show finished/0.
#show pr_impl/3.
#show nm/3.
