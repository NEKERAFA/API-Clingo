# Quine-McCluskey-Petrick in ASP

## Usage
Run ```python minterms.py INPUT_FILE```. Python 3.x and clingo 5.x are required.

The input file must contain the terms of the function to minimize in their binary representation, one term per line.
See the samples at the provided input folder for reference. The script can also handle "don't care" values, these
should be specified with an 'x' (i.e ```ab'c + a'b'``` translates to ```101 00x```)

The script will show the prime implicants for the provided minterms, extract the essential implicants and process the remaining implicants to achieve total coverage. Only a single minimal solution will be specified, to show all of the possible minimal solutions, use the ```--all``` parameter. Minimization method can be specified through the ```-m / --minmode``` parameter.

## TO DO
* Input files should contain boolean functions and not minterms?
