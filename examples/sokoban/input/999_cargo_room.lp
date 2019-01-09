%% x x x x x x x
%% x x       x x
%% x   b   b * x
%% x -   x   * x
%% x   b   b * x
%% x x       * x
%% x x x x x x x
%%
%% MAX 50 moves
%% Can be solved in 43

#const max = 50.
#const height = 6.
#const width = 6.

height(height). width(width).

row(0..H) :- height(H).
col(0..W) :- width(W).

box(a;b;c;d).

wall(R, (0;6)) :- row(R).
wall((0;6), C) :- col(C).
wall(1,1). wall(1,5). wall(5,1). wall(3,3).

start(3,1).
goal(2,5). goal(3,5). goal(4,5). goal(5,5).

box_start(a, 2, 2). box_start(b, 2, 4).
box_start(c, 4, 2). box_start(d, 4, 4).

moves(max).
