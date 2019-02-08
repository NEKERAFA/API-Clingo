#const maxstep = 1.

step(0..maxstep).
cell(1..width, 1..height).
tileid(C) :- tiletype(C, _).
extreme(C) :- tiletype(C, TT), 1{tilein(TT,D)}1.
cellcont(X, Y, C, 0) :- cell(X,Y), C=Y+((X-1)*width)-1.

%% Each step only generate a movement for one of the spaces in the board
%% Movement can't go out of the board or into a bolted tile
%% Do not generate movements if the circuit is closed
1 { move(C, D, T) : tiletype(C, space), cellcont(X,Y,C,T-1),
          direction(D), dirmove(D, DX, DY), C != DC,
          cellcont(X+DX, Y+DY, DC, T-1), not bolted(DC), not tiletype(DC, space) }1 :- step(T), T > 0, not closed(T-1).

%% Move the tile we moved the blank space against in the opposite direction
cellcont(X,Y,DC,T) :- cellcont(X,Y,C,T-1), cellcont(X+DX,Y+DY,DC,T-1), move(C,D,T), dirmove(D, DX, DY), step(T), T > 0.
moved(DC,T) :- cellcont(X,Y,C,T-1), cellcont(X+DX,Y+DY,DC,T-1), move(C,D,T), dirmove(D, DX, DY), step(T), T > 0.
%% Move the blank space
cellcont(X+DX,Y+DY,C,T) :- cellcont(X,Y,C,T-1), move(C,D,T), dirmove(D, DX, DY), step(T), T > 0.
moved(C,T) :- cellcont(X,Y,C,T-1), move(C,D,T), dirmove(D, DX, DY), step(T), T > 0.
%% Inertia, all the unmoved pieces stay the same.
cellcont(X,Y,C,T) :- cellcont(X,Y,C,T-1), not moved(C,T), dirmove(D, DX, DY), step(T), T > 0.

%% One tile is reachable form another if
%% 1. They are adjacent
%% 2. They have a pair of opposing tileins (e.g. T1 has down while T2 has up)
%%    that follow that direcion (in the example they should be vertically adjacent)

reach(C1, C2, T) :- cellcont(X1,Y1,C1,T), cellcont(X2,Y2,C2,T),
                    tiletype(C1, TT1), tiletype(C2, TT2), tilein(TT1, D1), tilein(TT2, D2),
                    dirmove(D1, D1X, D1Y), dirmove(D2, D2X, D2Y), D1X+D2X+D1Y+D2Y == 0,
                    D1 != D2, step(T), X2 == X1+D1X, Y2 == Y1+D1Y.

%% Transitive closure for reachability
reach(C1, C3, T) :- reach(C1, C2, T), reach(C2, C3, T), C1 < C3, step(T).
%% A circuit is closed if two different extremes can be reached from one another
closed(T) :- extreme(C1), extreme(C2), reach(C1,C2,T), C1 < C2.

reachstars(S) :- #count{ C2: reach(C1,C2,T), extreme(C1), star(C2) }=S, step(maxstep).

%% At maxstep the circuit must be closed
:- not closed(maxstep).
%% The step in which we close the circuit must be the last step.
:- closed(T1), closed(T2), T2 > T1.
%% Always grab 3 stars on the way
:- reachstars(S), S!=3.

#show move/3.
%#show reach/3.
%#show closed/1.
%#show reachstars/1.
