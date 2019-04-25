%% ID of the present minterms
id(X) :- m(X, _, _).
level(1..N) :- N=#count{ A: m(X,A,V) }.

%% How many ones and xs does the minterm have
ones(X, C) :- id(X), C=#count{ A:m(X, A, 1) }.
exes(X, C) :- id(X), C=#count{ A:m(X, A, x) }.

%% Match minterms that have a difference of a single one and same number of xs
%% This should help to not match ids of incompatible groups and steps
match(X, Y) :- ones(X, CX), ones(Y, CY), CX == CY-1,
                  exes(X, XX), exes(Y, XY), XX == XY.

%% Minterms are adjacent if they match and they only differ in a single position
adj(X, Y) :- match(X, Y), 1=#count{ A: m(X, A, V), m(Y, A, W), V != W }.

%% Generate the new minterm
%m((X,Y), A, x) :- adj(X, Y), m(X, A, V), m(Y, A, W), V!=W.
%m((X,Y), A, V) :- adj(X, Y), m(X, A, V), m(Y, A, W), V==W.
