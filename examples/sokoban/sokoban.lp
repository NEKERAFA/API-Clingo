%%%%%%%%%%%%%%%%%%%
%% S O K O B A N %%
%%%%%%%%%%%%%%%%%%%

% Generate
%% Generate one move to a valid position, one for each step
%% TODO: Can we define here that we can only move to adjacent tiles?
1 { move(X,Y,T) : row(X), col(Y) } 1 :- moves(M), T = 1..M.

% Define
%% Player starts at start position
player_on(X, Y, 0) :- start(X,Y).
%% Player is on the tile it moved into
player_on(X, Y, T) :- move(X,Y,T).

%% Check the direction in which we moved
%% This also serves as a proyection for the output
move_dir(up, T) :- player_on(X+1,Y,T-1), player_on(X,Y,T).
move_dir(down, T) :- player_on(X-1,Y,T-1), player_on(X,Y,T).
move_dir(left, T) :- player_on(X,Y+1,T-1), player_on(X,Y,T).
move_dir(right, T) :- player_on(X,Y-1,T-1), player_on(X,Y,T).

%% Boxes start at their respective start positions
box_on(ID, X, Y, 0) :- box_start(ID, X, Y).
%% Inertia, boxes stay on their place if they're not pushed
box_on(ID, X, Y, T+1) :- box_on(ID, X, Y, T), not move(X, Y, T+1), not moves(T).
%% Boxes move on the direction the player moved when it moved into their tiles
box_on(ID, X, Y+1, T+1) :- box_on(ID, X, Y, T), move(X, Y, T+1), move_dir(right, T+1).
box_on(ID, X, Y-1, T+1) :- box_on(ID, X, Y, T), move(X, Y, T+1), move_dir(left, T+1).
box_on(ID, X-1, Y, T+1) :- box_on(ID, X, Y, T), move(X, Y, T+1), move_dir(up, T+1).
box_on(ID, X+1, Y, T+1) :- box_on(ID, X, Y, T), move(X, Y, T+1), move_dir(down, T+1).

%% We can only move to adjacent tiles from where we are (4-direction)
valid_move(X+1, Y, T) :- player_on(X,Y,T), row(X+1), col(Y).
valid_move(X-1, Y, T) :- player_on(X,Y,T), row(X-1), col(Y).
valid_move(X, Y+1, T) :- player_on(X,Y,T), row(X), col(Y+1).
valid_move(X, Y-1, T) :- player_on(X,Y,T), row(X), col(Y-1).

% Test
%% Cannot move into walls
:- move(X,Y,T), wall(X,Y).
%% Cannot move to non-adjacent tiles
:- move(X,Y,T), not valid_move(X,Y,T-1).
%% Boxes cannot be moved into another boxes
:- box_on(ID1, X, Y, T), box_on(ID2, X, Y, T), ID1 != ID2.
%% Boxes cannot be moved into walls
:- box_on(ID, X, Y, T), wall(X,Y).
%% At the last step, all the boxes should be on goal tiles
:- moves(M), box(B), box_on(B, X, Y, M), not goal(X,Y).
