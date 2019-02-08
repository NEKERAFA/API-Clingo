# Roll the Ball in ASP

## Usage
Run ```clingo roll.lp tiles.lp INPUT_FILE -c maxsteps=N```, with N being the
exact number of steps in which the puxxle must be solved. clingo 5.x is required.

There is no parser for the input yet as I plan to develop a GUI for this one.
There is a sample puzzle located inside the input folder, you must specify height
and width as constants and then, indicate the type of tile present at the starting position.
In the predicate ```tiletype(ID, TYPE)```, ID is the unique identifier of the tile,
IDs are assigned sequentially, so ```ID = Y+((X-1)*width)-1``` (e.g. tile 0 is at
position (1,1), while tile 13 is at position (4,2) ). The tile types' names can
be found inside the ```tiles.lp``` file (for example a vertical pipe tile would
have the type 'vertical', a right-open extreme would be 'exright' and a tile
having both up and right openings would be 'upright').

Other than that you must also specify which tiles are bolted and which ones do
contain stars, these are indicated through ```bolted(ID)``` and ```star(ID)```
respectively.

## TO DO
* GUI with pyglet
