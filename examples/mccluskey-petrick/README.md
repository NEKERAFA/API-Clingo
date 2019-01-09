# McCluskey-Petrick in ASP

## Usage
Run ```python minterms.py INPUT_FILE```. Python 3.x and clingo 5.x are required.

The input file must contain the terms of the function to minimize in their binary representation, one term per line.
See the samples at the provided input folder for reference.

The script will show the prime implicants for the provided minterms, extract the essential implicants and process the
remaining implicants to achieve total coverage. In the case of multiple possible solutions, all of them will be specified.

## TO DO
* Input files should contain boolean functions and not minterms?
* Check if the current method guarantees that the solutions provided are minimal (They should be, but check)
* Adjust verbosity 
