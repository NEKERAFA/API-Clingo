#program base.
int(1..5).
p(5).
q(N) :- int(N), p(M), N < M.
