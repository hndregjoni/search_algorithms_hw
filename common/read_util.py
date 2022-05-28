from typing import List

def lines_to_int_grid(lines: List[str]) -> List[List[int]]:
    res: List[List[int]] = []

    for line in lines:
        res.append([])
        for fl in line.strip().split():
            res[-1].append(int(fl))
    
    # Transpose:
    res = list(map(list, zip(*res)))

    return res