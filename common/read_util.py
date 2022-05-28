from typing import List, Tuple, cast

def lines_to_int_grid(lines: List[str]) -> List[List[int]]:
    res: List[List[int]] = []

    for line in lines:
        res.append([])
        for fl in line.strip().split():
            res[-1].append(int(fl))
    
    # Transpose:
    res = list(map(list, zip(*res)))

    return res

def read_int_tuple(line: str, n: int) -> Tuple[int, ...]:
    splitted = line.strip().split()

    assert len(splitted) == n

    return tuple(map(int, splitted))

def read_int_twople(line: str) -> Tuple[int, int]:
    return cast(Tuple[int, int], read_int_tuple(line, 2))