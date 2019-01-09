impl_id(X) :- impl(X, _).
m_id(I) :- impl(_, I).

overlapping_impl_ids(X, Y) :- impl(X,I), impl(Y,I), X<Y.

1{ selected_impl_id(X):impl(X,I) }.

selected_impl(X, I) :- selected_impl_id(X), impl(X, I).

total_coverage :- C=#count{I:m_id(I)}, D=#count{J:selected_impl(_,J)}, C=D.

:- selected_impl_id(X), selected_impl_id(Y), X<Y, overlapping_impl_ids(X,Y).
:- not total_coverage.

#show selected_impl/2.
#show total_coverage/0.
