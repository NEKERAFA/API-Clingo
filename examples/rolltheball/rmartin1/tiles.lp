direction(up; down; right; left).
dirmove(up, -1, 0). dirmove(down, 1, 0).
dirmove(right, 0, 1). dirmove(left, 0, -1).

tiletype(exleft; exright; exup; exdown).
tiletype(block; space; vertical, horizontal).
tyletype(downright; leftdown; upright; leftup).

tilein(exleft, left). tilein(exright, right).
tilein(exup, up). tilein(exdown, down).
tilein(vertical, up). tilein(vertical, down).
tilein(horizontal, left). tilein(horizontal, right).
tilein(downright, down). tilein(downright, right).
tilein(leftdown, left). tilein(leftdown, down).
tilein(upright, up). tilein(upright, right).
tilein(leftup, left). tilein(leftup, up).
