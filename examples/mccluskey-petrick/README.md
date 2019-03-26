# Quine-McCluskey-Petrick in ASP

## Usage
Run ```python minterms.py INPUT_FILE```. Python 3.x and clingo 5.x are required.

The input file must contain the terms of the function to minimize in their binary representation, one term per line.
See the samples at the provided input folder for reference. The script can also handle already grouped values, these
should be specified with an 'x' (i.e ```ab'c + a'b'``` translates to ```101 00x```)

These input files specify the on-set for the logic formula and optionally the dont-care-set, with the offset
being left out as it would be the complimentary set of minterms of the union of the on-set and dont-care-set.
To specify the dont-care-set, add a line with a single ```d``` character and then specify the dont-care minterms.
An example of this can be found in the input folder (```bike.txt```)

The script will show the prime implicants for the provided minterms, extract the essential implicants and process the remaining implicants to achieve total coverage. Only a single minimal solution will be specified, to show all of the possible minimal solutions, use the ```--all``` parameter. Minimization method can be specified through the ```-m / --minmode``` parameter.

Additional scripts like a random sampler and a minterms-to-logic-facts can be found in the helper folder.

## TO DO
* Input files should contain boolean functions and not minterms?
