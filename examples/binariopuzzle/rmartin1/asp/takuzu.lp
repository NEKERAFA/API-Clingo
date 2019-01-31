%%
%% round tiles, black and white
%% unrepeated, unequal
%% a s p solved
%%

%% DEFINE
color(b;w).
%% size(X) is provided by the input file
cell(1..X, 1..X) :- size(X).
row(1..X) :- size(X).
col(1..X) :- size(X).

%% GENERATE
%% Generate a single tile per cell, choose a color.
%% The tiles already provided are not decided upon.
1{ tile(X,Y,C) : color(C) }1 :- cell(X,Y).
%% Define horizontal and vertical adjacencies by color
%% Adjacent tiles are one step away and also the ones that are transitively adjacent
color_adj(X,Y1, X,Y2, C) :- tile(X,Y1,C), tile(X,Y2,C), Y1 == Y2-1.
color_adj(X,Y1, X,Y3, C) :- color_adj(X,Y1, X,Y2, C), color_adj(X,Y2, X,Y3, C).
color_adj(X1,Y, X2,Y, C) :- tile(X1,Y,C), tile(X2,Y,C), X1 == X2-1.
color_adj(X1,Y, X3,Y, C) :- color_adj(X1,Y, X2,Y, C), color_adj(X2,Y, X3,Y, C).

%% TEST
%% All tiles must be covered
:- cell(X,Y), not tile(X,Y,_).
%% Each row and column must have the same number of black and white tiles
:- row(X), B=#count{ Y:tile(X,Y,C), C == b }, W=#count{ Y:tile(X,Y,C), C == w }, B!=W.
:- col(Y), B=#count{ X:tile(X,Y,C), C == b }, W=#count{ X:tile(X,Y,C), C == w }, B!=W.
%% Do not allow repeated patterns in rows and columns
:- row(X1), row(X2), X1 < X2, #count{Y: tile(X1,Y,C), tile(X2,Y,C)}=S, size(S).
:- col(Y1), col(Y2), Y1 < Y2, #count{X: tile(X,Y1,C), tile(X,Y2,C)}=S, size(S).
%% Color adjacencies cannot be of length greater than 2
:- color_adj(X1, Y1, X2, Y2, C), D=(X2-X1)+(Y2-Y1)+1, D > 2.

#show tile/3.
