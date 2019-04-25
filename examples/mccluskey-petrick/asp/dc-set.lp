val(0;1).
var(A) :- m(X, A, V).
id(X) :- m(X, A, V).
%% Los guiones son un problema, hay que desdoblar primero los guiones presentes?
%% No generar dcids que matcheen con minterms con guiones?
dcid(X) :- X > 0.
