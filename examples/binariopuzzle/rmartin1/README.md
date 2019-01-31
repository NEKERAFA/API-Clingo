# Binario/Takuzu Puzzle

## Usage
Run ```python takuzu.py INPUT_FILE```. Python 3.x and clingo 5.x are required.
For more options, use ```--help```.
```
usage: takuzu.py [-h] [-n N] [-s] I

Solve some binarios

positional arguments:
  I                   route for the binario puzzle instance

optional arguments:
  -h, --help          show this help message and exit
  -n N, --num_sols N  number of solutions requested, only one is provided by
                      default. 0 means "all the solutions"
  -s, --stats         print solver stats

```

## Input
There are some sample input files provided that can be used as sample but the
format is the following:
```
4
0...
..1.
....
1...
```

The first line must contain only the size of the puzzle, since the puzzles are
always squares, there is no need to specify height and width.
The remaining lines represent the actual puzzle input, where 0 means a white
tile, 1 means a black tile and . means a blank cell that the program must fill.

## TODO
Maybe include some simple GUI
