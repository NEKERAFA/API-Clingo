#const width = 4.
#const height = 4.

tile(0..12). space(13). tile(14; 15).

tilein(0, down).
tilein(4, up). tilein(4,down).
tilein(8, up). tilein(8,down).
tilein(9, left). tilein(9,right).
tilein(12, up). tilein(12,right).
tilein(14, left). tilein(14, right).
tilein(15, left).

posini(0, 1, 1). posini(1, 1, 2). posini(2, 1, 3). posini(3, 1, 4).
posini(4, 2, 1). posini(5, 2, 2). posini(6, 2, 3). posini(7, 2, 4).
posini(8, 3, 1). posini(9, 3, 2). posini(10, 3, 3). posini(11, 3, 4).
posini(12,4, 1). posini(13, 4, 2). posini(14, 4, 3). posini(15, 4, 4).

bolted(0). bolted(14). bolted(15).
star(4). star(9). star(14).
