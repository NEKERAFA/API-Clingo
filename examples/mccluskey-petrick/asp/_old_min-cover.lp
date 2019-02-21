impl_id(X) :- impl(X, _).
m_id(I) :- impl(_, I).

dupe_impl(I) :- impl_id(X), impl_id(Y), X<Y, impl(X, I), impl(Y, I).

uni_impl(X) :- impl(X, I), not dupe_impl(I).
covered_minterm(I) :- m_id(I), uni_impl(X), impl(X,I).
uncovered_minterm(I) :- m_id(I), impl(X,I), not covered_minterm(I).

essn_impl(X, I) :- impl(X,I), uni_impl(X).
left_impl_id(X) :- impl(X,I), uncovered_minterm(I).
left_impl(X, I) :- impl(X,I), left_impl_id(X).

total_coverage :- C=#count{I:m_id(I)}, D=#count{J:covered_minterm(J)}, C=D.

#show essn_impl/2.
#show left_impl/2.
#show total_coverage/0.
